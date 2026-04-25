
base_dir = 'dataset'
os.makedirs(base_dir, exist_ok=True)
for category in dataset_ids.keys():
    os.makedirs(os.path.join(base_dir, category), exist_ok=True)

async def fetch_pdb(session, pdb_id, category):
    url = f'https://files.rcsb.org/download/{pdb_id.upper()}.pdb'
    filepath = os.path.join(base_dir, category, f'{pdb_id.upper()}.pdb')
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                async with aiofiles.open(filepath, 'w') as f:
                    await f.write(content)
                return True, pdb_id
            else:
                return False, f"{pdb_id} (Status: {response.status})"
    except Exception as e:
        return False, f"{pdb_id} (Error: {str(e)})"


async def main():
    print(f"Starting concurrent extraction of {sum(len(ids) for ids in dataset_ids.values())} structures...")
    async with aiohttp.ClientSession() as session:
        tasks = []
        for category, ids in dataset_ids.items():
            for pdb_id in ids:
                tasks.append(fetch_pdb(session, pdb_id, category))
        
        results = await asyncio.gather(*tasks)
        
        successes = [r[1] for r in results if r[0]]
        failures = [r[1] for r in results if not r[0]]
        
        print(f"\nExtraction Complete.")
        print(f"Successfully downloaded: {len(successes)} structures.")
        if failures:
            print(f"Failed to download: {failures}")

await main()
