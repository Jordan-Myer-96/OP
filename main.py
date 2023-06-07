import requests
import time
# Define API key globally
API_KEY = "RGAPI-020113b1-90c9-4cc4-b087-1c6d3133a9fe"  # Replace with your API key

def get_summoner_id(summoner_name):
    base_url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data['accountId']
    else:
        print("Error Code", response.status_code)
        return None

def get_match_history(encrypted_account_id, limit):
    base_url = f"https://na1.api.riotgames.com/lol/match/v5/matchlists/by-account/{encrypted_account_id}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        matches = data['matches'][:limit]  # Limit the number of matches
        for match in matches:
            print("Match ID:", match['gameId'])
    else:
        print("Error Code", response.status_code)

# Usage
summoner_name = "LightNephilim"  # Replace with your summoner name
limit = 1  # Replace with the number of matches you want

print(get_summoner_id(summoner_name))
get_match_history("hjIaLvoOPcnjZOyY-vEjBl3T7FrV0T0KJSfUoHBrW_LaUyo",1)
encrypted_account_id = get_summoner_id(summoner_name)
if encrypted_account_id:
    time.sleep(1)
    get_match_history(encrypted_account_id, limit)
