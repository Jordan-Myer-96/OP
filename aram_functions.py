import requests
import time
import json
import datetime
import pickle

# Define API key globally
API_KEY = "RGAPI-d4c56a04-1227-400c-b541-c38b65337c81"  # Replace with your API key

def download_champion_data():
    base_url = "http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        with open('champion.json', 'w') as f:
            json.dump(data, f)
        return data
    else:
        print("Error Code", response.status_code)
        return None

def get_summoner_id(summoner_name):
    base_url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['puuid']
    else:
        print("Error Code", response.status_code)
        return None
    
def get_match_history(summoner_name,limit):

    puuid = get_summoner_id(summoner_name)
    base_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={limit}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(base_url, headers=headers)


    if response.status_code == 200:
        data = response.json()
        return(data)
        #matches = data[] # Limit the number of matches
        # for match in data:
        #     print(match)
    else:
        print("Error Code", response.status_code)  
        return(None)


def get_matches_with_summoners(match_ids, summoner_names):
    """Find matches where all the specified summoners participated."""
    matches_with_summoners = []
    match_details = []  # list to hold match details
    
    for match_id in match_ids:
        base_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
        headers = {
            "X-Riot-Token": API_KEY
        }
        response = requests.get(base_url, headers=headers)

    
        # Add a delay after each request to prevent hitting rate limit
        time.sleep(1.2)

        if response.status_code == 200:
            data = response.json()
            participants = [participant['summonerName'] for participant in data['info']['participants']]
            # Check if all summoner_names are in participants
            if all(summoner in participants for summoner in summoner_names):
                matches_with_summoners.append(match_id)
                # Get relevant details and store in the match details list
                for summoner in summoner_names:
                    for participant in data['info']['participants']:
                        if participant['summonerName'] == summoner:
                            match_details.append({
                                'match_id': match_id,
                                'game_creation': datetime.datetime.fromtimestamp(data['info']['gameCreation'] / 1000).strftime('%Y-%m-%d %H:%M'),
                                'summoner_name': summoner,
                                'win': participant['win'],
                                'champion': champion_id_to_name.get(str(participant['championId']), 'Unknown champion'),
                                'kills': participant['kills'],
                                'assists': participant['assists'],
                                'deaths': participant['deaths'],
                                'champ_damage': participant['totalDamageDealtToChampions']
                            })

        else:
            print("Error Code", response.status_code)
    
    # Compute win rate
    total_games = len(match_details)
    total_wins = sum(detail['win'] for detail in match_details)
    win_rate = total_wins / total_games * 100
    
    return matches_with_summoners, match_details, win_rate

def consolidate_details(match_details):
    consolidated_details = {}
    for detail in match_details:
        match_id = detail['match_id']
        if match_id not in consolidated_details:
            consolidated_details[match_id] = {
                'game_creation': detail['game_creation'],
                'win': detail['win'],
                'summoner_details': {}
            }
        summoner_name = detail['summoner_name']
        summoner_details = {
            'champion': detail['champion'],
            'kills': detail['kills'],
            'assists': detail['assists'],
            'deaths': detail['deaths'],
            'champ_damage': detail['champ_damage']
        }
        consolidated_details[match_id]['summoner_details'][summoner_name] = summoner_details

    return consolidated_details
    
#champion_data = download_champion_data()
with open('champion.json', 'r') as f:
    champion_data = json.load(f)
champion_id_to_name = {v['key']: k for k, v in champion_data['data'].items()}
