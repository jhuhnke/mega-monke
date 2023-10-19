import requests
import pandas as pd
from decouple import config

# Load the API key from the .env file
api_key = config('API_KEY')

# Helius URL for getting the mint list
mint_list_url = f"https://api.helius.xyz/v1/mintlist?api-key={api_key}"

# Helius RPC URL
rpc_url = f"https://rpc.helius.xyz/?api-key={api_key}"

timeout = 30
rpc_timeout = 60  # Timeout for RPC request

# Maximum number of retry attempts
max_retries = 20

# Delay between retry attempts (in seconds)
retry_delay = 20  # Adjust this value as needed

# Function to fetch mints based on creators and minimum count
def fetch_mints(creators, min_count):
    response = requests.post(mint_list_url, json={
        "query": {
            "firstVerifiedCreators": creators,
        },
        "options": {
            "limit": 10000,  # Adjust the limit as needed
        }
    }, timeout=timeout)

    if response.status_code == 200:
        data = response.json()
        mints = [item["mint"] for item in data["result"]]
        return mints
    else:
        print("API request failed:", response.status_code)
        return []

# Gen2 Creators
creators_gen2 = ["mdaoxg4DVGptU4WSpzGyVpK3zqsgn7Qzx5XNgWTcEA2"]
mint_list_gen2 = fetch_mints(creators_gen2, 5)

# Gen3 Creators
creators_gen3 = ["HV4Nvm9zHfNA43JYYkjZu8vwqiuE8bfEhwcKFfyQ65o5"]
mint_list_gen3 = fetch_mints(creators_gen3, 50)

# Function to fetch holders for a list of mints
def fetch_holder(address):
    asset_id = address
    response = requests.post(rpc_url, json={
        "jsonrpc": "2.0",
        "id": "my-id",
        "method": "getAsset",
        "params": [asset_id],
    }, timeout=rpc_timeout)  # Set the timeout here

    if response.status_code == 200:
        data = response.json()
        owner = data["result"]["ownership"]["owner"]
        return owner
    else:
        print(f"API request for mint {address} failed:", response.status_code)
        return None

# Function to fetch holders for a list of mints
def fetch_holders(mint_list):
    holder_counts = {}

    for mint in mint_list:
        retries = 0
        while retries < max_retries:
            try:
                owner = fetch_holder(mint)
                if owner:
                    if owner in holder_counts:
                        holder_counts[owner] += 1
                    else:
                        holder_counts[owner] = 1
                    break  # Success, break out of retry loop
                else:
                    print(f"RPC request for mint {mint} returned None.")
            except requests.exceptions.Timeout:
                print(f"RPC request for mint {mint} timed out, retrying in {retry_delay} seconds...")
                retries += 1
                time.sleep(retry_delay)

        if retries >= max_retries:
            print(f"Max retries reached for mint {mint}, unable to fetch holder address.")

    return holder_counts

# Gen2 Holders
holder_counts_gen2 = fetch_holders(mint_list_gen2)
gen2_holders = [address for address, count in holder_counts_gen2.items() if count >= 5]
print(len(gen2_holders))

# Gen3 Holders
holder_counts_gen3 = fetch_holders(mint_list_gen3)
gen3_holders = [address for address, count in holder_counts_gen3.items() if count >= 50]
print(len(gen3_holders))

# Create a DataFrame for the new data
new_data = pd.DataFrame({
    'date': [pd.Timestamp.now()],
    'gen_2_mega_monkes': [gen2_holders],
    'gen_3_mega_monkes': [gen3_holders],
    'total_mega_monkes': [len(gen2_holders) + len(gen3_holders)]
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