class MultiChainSelect(Select):
    def __init__(self, target_chains):
        self.target_chains = list(target_chains)

    def accept_chain(self, chain):
        if chain.get_id() in self.target_chains:
            return 1
        return 0
        
    def accept_residue(self, residue):
        if residue.id[0] != " ":
            return 0
        return 1

def isolate_chains(filepath, target_chains):
    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure('protein', filepath)
        io = PDBIO()
        io.set_structure(structure)
        io.save(filepath, MultiChainSelect(target_chains))
        return True
    except Exception as e:
        print(f"Error slicing {filepath}: {e}")
        return False

# 3. The Universal Execution Loop
base_dir = 'dataset'
total_success = 0
total_files = 0



# Walk through every subdirectory in the dataset folder
for root, dirs, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith('.pdb'):
            total_files += 1
            pdb_id = filename[:4].upper()
            filepath = os.path.join(root, filename)
            
            if pdb_id in master_chain_map:
                if isolate_chains(filepath, master_chain_map[pdb_id]):
                    total_success += 1
            else:
                print(f"Warning: {pdb_id} in {root} not found in master map.")

print(f"\nUniversal Slice Complete.")
