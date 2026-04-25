

with open("dataset_split_manifest.json", 'r') as f:
    manifest = json.load(f)


ordered_items = manifest["train"] + manifest["val"]

parser = PDBParser(QUIET=True)
lengths = []

print("Extracting sequence lengths in strict tensor alignment...")
for item in ordered_items:
    pdb_path = item["path"]
    try:
        s = parser.get_structure('p', pdb_path)
        # Count only standard amino acid residues
        length = sum(1 for r in s.get_residues() if r.id[0] == ' ')
        lengths.append(length)
    except Exception as e:
        print(f"Error parsing {pdb_path}: {e}")

print(f"Successfully extracted {len(lengths)} aligned lengths.")
lengths = np.array(lengths, dtype = float)

dim103_values = X_all_dec[:, 103]

# Correlation with sequence length
corr_length, p_length = pearsonr(lengths, dim103_values)
print(f"Dim 103 vs sequence length: r={corr_length:.3f}, p={p_length:.4f}")

# Correlation with label (y_all is already perfectly aligned)
corr_label, p_label = pointbiserialr(y_all, dim103_values)
print(f"Dim 103 vs malign label:    r={corr_label:.3f}, p={p_label:.4f}")

# The True Ratio
if abs(corr_length) > abs(corr_label):
    print(f"\nDim 103 tracks length {abs(corr_length)/abs(corr_label):.1f}x more than biology")
else:
    print(f"\nDim 103 tracks biology {abs(corr_label)/abs(corr_length):.1f}x more than length")
