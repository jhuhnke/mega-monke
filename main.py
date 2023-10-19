import requests
import pandas as pd
from decouple import config

# Load the API key from the .env file
api_key = config('API_KEY')

# Helius RPC URL
rpc_url = f"https://rpc.helius.xyz/?api-key={api_key}"

rpc_timeout = 60  # Timeout for RPC request

# Maximum number of retry attempts
max_retries = 20

# Delay between retry attempts (in seconds)
retry_delay = 20  # Adjust this value as needed

# Function to fetch owners for a list of assets based on collection ID and minimum count
def fetch_owners(collection_id, min_count):
    page = 1
    owners = []

    while True:
        response = requests.post(rpc_url, json={
            "jsonrpc": "2.0",
            "id": "my-id",
            "method": "getAssetsByGroup",
            "params": {
                "groupKey": "collection",
                "groupValue": collection_id,
                "page": page,
                "limit": 1000,
            },
        }, timeout=rpc_timeout)

        if response.status_code != 200:
            print(f"RPC request failed with status code {response.status_code}")
            return []

        data = response.json()
        assets = data.get("result", {}).get("items", [])

        for asset in assets:
            owner = asset.get('ownership', {}).get('owner')
            owners.append(owner)

        if len(assets) < 1000:
            break  # Reached the end of the collection

        page += 1

    return owners

# Gen2 Collection ID (Replace with your actual Gen2 collection ID)
collection_id_gen2 = "SMBtHCCC6RYRutFEPb4gZqeBLUZbMNhRKaMKZZLHi7W"
owners_gen2 = fetch_owners(collection_id_gen2, 1)
gen2_holders = [address for address in owners_gen2 if owners_gen2.count(address) >= 5]

# Gen3 Collection ID (Replace with your actual Gen3 collection ID)
collection_id_gen3 = "8Rt3Ayqth4DAiPnW9MDFi63TiQJHmohfTWLMQFHi4KZH"
owners_gen3 = fetch_owners(collection_id_gen3, 1)
gen3_holders = [address for address in owners_gen3 if owners_gen3.count(address) >= 50]

# Merge all mega monkes and deduplicate
all_mega_monkes = list(set(gen2_holders + gen3_holders))

# Find double mega monke (common wallets in both Gen2 and Gen3)
double_mega_monke = list(set(gen2_holders) & set(gen3_holders))

# Create a DataFrame for the new data
new_data = pd.DataFrame({
    'date': [pd.Timestamp.now()],
    'gen_2_mega_monkes': [gen2_holders],
    'gen_3_mega_monkes': [gen3_holders],
    'all_mega_monkes': [all_mega_monkes],
    'double_mega_monkes': [double_mega_monke],
    'total_mega_monkes': [len(all_mega_monkes)]
})

# Load the existing .csv file if it exists
try:
    existing_data = pd.read_csv('mega_monke_stats.csv')
except FileNotFoundError:
    existing_data = pd.DataFrame()

# Concatenate the new data on top of the existing data
combined_data = pd.concat([new_data, existing_data], ignore_index=True)

# Save the combined data to the .csv file
combined_data.to_csv('mega_monke_stats.csv', index=False)