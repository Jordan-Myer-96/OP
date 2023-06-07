import os
import pickle
import aram_functions as af

regenerate_data = True

if regenerate_data and os.path.exists('match_data.pkl'):
    os.remove('match_data.pkl')

if os.path.exists('match_data.pkl'):
    # Load match_details from file
    with open('match_data.pkl', 'rb') as f:
        matches_with_summoners, match_details, win_rate = pickle.load(f)      
else:
    # Generate match_details
    limit = 50
    summoner_name = "Zero Jg Pressure"  # replace with the actual summoner name
    summoner_names = ["Zero Jg Pressure","Nickozz"]

    match_history = af.get_match_history(summoner_name,limit)
    matches_with_summoners, match_details, win_rate = af.get_matches_with_summoners(match_history,summoner_names)
    # Save match_details to file
    with open('match_data.pkl', 'wb') as f:
        pickle.dump((matches_with_summoners, match_details, win_rate), f)

print(match_details)

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

# Print the consolidated details
for match_id, details in consolidated_details.items():
    print(f"Match {match_id}:")
    print(f"  Game Creation: {details['game_creation']}")
    print(f"  Win: {'Yes' if details['win'] else 'No'}")
    for summoner_name, summoner_details in details['summoner_details'].items():
        print(f"  {summoner_name}: {summoner_details}")
    print()

# Print the summary
print(f"Summoners {', '.join(summoner_names)} have played {len(matches_with_summoners)} of the last {limit} games together.")
print(f"Their win rate as a group is {win_rate:.2f}%.")

