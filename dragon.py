import requests
import time

API_KEY = "RGAPI-020113b1-90c9-4cc4-b087-1c6d3133a9fe"  # Your API key
def download_champion_data():
    base_url = "http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion.json"  # Change this if a new version of dDragon is available
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error Code", response.status_code)
        return None
champion_data = download_champion_data()
champion_id_to_name = {v['key']: k for k, v in champion_data['data'].items()}
time.sleep(1) 

print(champion_id_to_name)
