import requests
import pandas as pd

api_base_url = "https://pro-api.solscan.io/v1.0/public/nft/collection/stats?collectionId="

# Collection Ids
collectionIdGen2 = "9f58ed1881686dbdb84be7508bf0dc6bdaa175c96fd15fff483bc133063016ba"
collectionIdGen3 = "e46c6b445d7b8c6528d29e8ee5808a7a25597f56f9a4faec7d7f7852b7b055c6"

# Function to fetch holders based on collection and minimum count
def fetch_holders(collection_id, min_count):
    url = f"{api_base_url}{collection_id}&filter=holders"
    response = requests.get(url)
    data = response.json()

    if 'data' in data and 'data' in data['data']:
        holders = data['data']['data']
        filtered_holders = [holder for holder in holders if int(holder['value']) >= min_count]
        return [holder['wallet_address'] for holder in filtered_holders]
    else:
        return []

# Find holders for Gen2 with 5 or more monkeys
gen2_holders = fetch_holders(collectionIdGen2, 5)

# Find holders for Gen3 with 50 or more monkeys
gen3_holders = fetch_holders(collectionIdGen3, 50)

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