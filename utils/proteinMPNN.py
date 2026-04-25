
os.makedirs('vanilla_model_weights', exist_ok=True)

url = 'https://github.com/dauparas/ProteinMPNN/raw/main/vanilla_model_weights/v_48_020.pt'
urllib.request.urlretrieve(url, 'vanilla_model_weights/v_48_020.pt')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
checkpoint_path = '/content/ProteinMPNN/vanilla_model_weights/v_48_020.pt'
checkpoint = torch.load(checkpoint_path, map_location=device)


hidden_dim = 128
num_layers = 3
vocab = 21 

# The checkpoint saves the neighbor count as 'num_edges', not 'num_neighbors'
# We use .get() to safely default to 48 (the standard) just in case
k_neighbors = checkpoint.get('num_edges', 48)

# 2. Instantiate the empty PyTorch Model
model = ProteinMPNN(
    num_letters=vocab,
    node_features=hidden_dim,
    edge_features=hidden_dim,
    hidden_dim=hidden_dim,
    num_encoder_layers=num_layers,
    num_decoder_layers=num_layers,
    k_neighbors=k_neighbors,
    augment_eps=0.0, # CRITICAL: Set noise to 0 for deterministic extraction
    dropout=0.0      # CRITICAL: Turn off dropout completely
).to(device)

# 3. Load the trained weights
model.load_state_dict(checkpoint['model_state_dict'])
model.eval() 
