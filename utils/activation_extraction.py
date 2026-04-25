
protein_lengths = []
def extract_dual_representations(manifest_path, split_type, model, device):
    with open(manifest_path, 'r') as f:
        data = json.load(f)
    items = data[split_type]
    
    X_encoder_features = []
    X_decoder_features = []
    y_labels = []
    failed_proteins = []
    
    with torch.no_grad():
        for item in tqdm(items, desc=f"Extracting {split_type.upper()} Vectors"):
            pdb_path = item["path"]
            label = item["label"]
            pdb_id = os.path.basename(pdb_path)[:4]
            
            try:
                # 1. Native MPNN Parsing
                pdb_dict_list = parse_PDB(pdb_path) 
                
                # 2. Convert to Spatial Graph
                batched_data = tied_featurize(pdb_dict_list, device, chain_dict=None)
                X, S, mask, lengths, chain_M, chain_encoding_all, chain_list_list, visible_list_list, masked_list_list, masked_chain_length_list_list, chain_M_pos, omit_AA_mask, residue_idx, dihedral_mask, tied_pos_list_of_lists_list, pssm_coef, pssm_bias, pssm_log_odds_all, bias_by_res_all, tied_beta = batched_data
                
                # 3. TRIGGER THE FORWARD HOOKS (BUG FIXED)
                # We generate a 2D noise tensor matching the sequence length, NOT the 4D coordinates.
                randn_1 = torch.randn(chain_M.shape, device=device)
                
                # Pass all 7 required arguments safely
                _ = model(X, S, mask, chain_M*chain_M_pos, residue_idx, chain_encoding_all, randn_1)
                
                # 4. Pull the NumPy arrays from your custom cache
                enc_out = activation_cache['encoder']['eval_vectors'] 
                dec_out = activation_cache['decoder']['eval_vectors'] 
                
                # 5. Masked Mean-Pooling (With Zero-Division Safety)
                mask_np = mask.cpu().numpy() 
                mask_expanded = np.expand_dims(mask_np, axis=-1) 
                
                # Use np.maximum to ensure we never divide by zero on a corrupted graph
                valid_nodes_count = np.maximum(np.sum(mask_np, axis=1, keepdims=True), 1)
                
                pooled_enc = np.sum(enc_out * mask_expanded, axis=1) / valid_nodes_count
                pooled_dec = np.sum(dec_out * mask_expanded, axis=1) / valid_nodes_count
                
                # 6. Store the flat 128-dim vectors
                X_encoder_features.append(pooled_enc[0])
                X_decoder_features.append(pooled_dec[0])
                y_labels.append(label)
                actual_length = int(mask.sum().item())
                protein_lengths.append(actual_length)
                # 7. Hardware Safety Flush
                del X, S, mask, batched_data, randn_1
                torch.cuda.empty_cache()
                
            except Exception as e:
                failed_proteins.append(f"{pdb_id} (Error: {str(e)})")
                continue

    # 8. EXPOSED ERROR LOGGER
    if failed_proteins:
        print(f"\n[WARNING] {split_type} extraction failed on {len(failed_proteins)} files. First 3 errors:")
        for err in failed_proteins[:3]:
            print(f" -> {err}")
    
    # 9. VSTACK SAFETY CHECK
    if len(X_encoder_features) == 0:
        print(f"[FATAL] Zero features extracted for {split_type}. Cannot stack arrays.")
        return None, None, None
        
    return np.vstack(X_encoder_features), np.vstack(X_decoder_features), np.array(y_labels), np.array(protein_lengths)


manifest_file = "dataset_split_manifest.json"
output_dir = "extracted_tensors"
os.makedirs(output_dir, exist_ok=True)

print("--- Firing Training Set Extraction ---")
train_results = extract_dual_representations(manifest_file, "train", model, device)

if train_results[0] is not None:
    X_train_enc, X_train_dec, y_train, lengths_train = train_results
    np.save(f"{output_dir}/X_train_encoder.npy", X_train_enc)
    np.save(f"{output_dir}/X_train_decoder.npy", X_train_dec)
    np.save(f"{output_dir}/y_train.npy", y_train)
    print(f"Train Array (Encoder): {X_train_enc.shape}")

print("\n--- Firing Validation Set Extraction ---")
val_results = extract_dual_representations(manifest_file, "val", model, device)

if val_results[0] is not None:
    X_val_enc, X_val_dec, y_val, lengths_val = val_results
    np.save(f"{output_dir}/X_val_encoder.npy", X_val_enc)
    np.save(f"{output_dir}/X_val_decoder.npy", X_val_dec)
    np.save(f"{output_dir}/y_val.npy", y_val)
    print(f"Validation Array (Encoder): {X_val_enc.shape}")

print("\n[SUCCESS] Script complete.")
