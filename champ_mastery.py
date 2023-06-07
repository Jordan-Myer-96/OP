from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)

API_KEY = "RGAPI-020113b1-90c9-4cc4-b087-1c6d3133a9fe"

def get_summoner_id(summoner_name):
    base_url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['id']  
    else:
        print("Error Code", response.status_code)
        return None

def get_highest_mastery(summoner_id):
    base_url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        highest_mastery = data[0]  # The champion masteries are sorted by points descending.
        champion_name = champion_id_to_name.get(str(highest_mastery['championId']), 'Unknown champion')
        points = highest_mastery['championPoints']
        champion_key = champion_id_to_name.get(str(highest_mastery['championId']))
        return champion_name, points, champion_key
    else:
        print("Error Code", response.status_code)
        return None, None, None

def download_champion_data():
    base_url = "http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    }

    # Set a maximum number of attempts
    max_attempts = 5

    for attempt in range(max_attempts):
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()  # Will raise an exception if the HTTP status code is 4xx or 5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed with error: {e}. Attempt {attempt + 1} of {max_attempts}.")
            time.sleep(5)  # Wait for a bit before retrying (this is often a good idea)

    # If we reached this point, all attempts failed.
    print(f"All {max_attempts} attempts failed. Unable to download champion data.")
    return None



champion_data = download_champion_data()
champion_id_to_name = {v['key']: k for k, v in champion_data['data'].items()}

@app.route('/', methods=['GET', 'POST'])
def index():
    champion_name = None
    points = None
    champion_key = None
    if request.method == 'POST':
        summoner_name = request.form.get('summoner_name')
        if summoner_name:
            summoner_id = get_summoner_id(summoner_name)
            time.sleep(1)
            if summoner_id:
                champion_name, points, champion_key = get_highest_mastery(summoner_id)
    return render_template('index.html', champion_name=champion_name, points=points, champion_key=champion_key)

if __name__ == '__main__':
    app.run(debug=True)
