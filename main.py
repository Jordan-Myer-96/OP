import os
import pickle
from aram_functions import get_summoner_id, get_match_history, get_matches_with_summoners, consolidate_details

regenerate_data = True
limit = 50

#"Zero Jg Pressure", "LightNephilim", "Nickozz","Pueo","Zhanababy"

summoner_name = "LightNephilim"  # match history to look through
summoner_names = ["Zero Jg Pressure", "LightNephilim", "Nickozz","Pueo","Zhanababy"]

if regenerate_data and os.path.exists('match_data.pkl'):
    os.remove('match_data.pkl')

if os.path.exists('match_data.pkl'):
    # Load match_details from file
    with open('match_data.pkl', 'rb') as f:
        matches_with_summoners, match_details, win_rate = pickle.load(f)      
else:
    # Generate match_details
    
    match_history = get_match_history(summoner_name,limit)
    matches_with_summoners, match_details, win_rate = get_matches_with_summoners(match_history,summoner_names)
    # Save match_details to file
    with open('match_data.pkl', 'wb') as f:
        pickle.dump((matches_with_summoners, match_details, win_rate), f)


consolidated_details = consolidate_details(match_details)
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

