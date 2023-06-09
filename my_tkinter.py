import tkinter as tk
from tabulate import tabulate
from aram_functions import get_summoner_id, get_match_history, get_matches_with_summoners, consolidate_details

consolidated_details = None

# Function to handle the button click event
def search_matches():
    limit = int(limit_var.get())
    summoner_name = summoner_var.get()
    summoner_names = summoner_names_var.get().split(',')

    # Call your existing functions here to get match_details and win_rate
    match_history = get_match_history(summoner_name, limit)
    matches_with_summoners, match_details, win_rate = get_matches_with_summoners(match_history, summoner_names)

    # Consolidate the match details
    consolidated_details = consolidate_details(match_details)

    # Display win_rate in a tkinter label
    win_rate_label.config(text=f"Win Rate: {win_rate}%")

    # Create a list to store the table data
    table_data = []

    # Iterate over the consolidated details and format the data for the table
    for match_id, match_info in consolidated_details.items():
        row = [
            f"Match {match_id}",
            match_info['game_creation'],
            'Yes' if match_info['win'] else 'No',
        ]
        for summoner_name, summoner_info in match_info['summoner_details'].items():
            row.extend([
                summoner_name,
                summoner_info['champion'],
                summoner_info['kills'],
                summoner_info['assists'],
                summoner_info['deaths'],
                summoner_info['champ_damage']
            ])
        table_data.append(row)

    # Format the table using tabulate
    table = tabulate(table_data, headers=["Match ID", "Game Creation", "Win", "Summoner Name", "Champion", "Kills", "Assists", "Deaths", "Champion Damage"], tablefmt="pretty")
    table_label.config(text=table)

# Create the Tkinter window
root = tk.Tk()

# Create StringVars for the entry fields
limit_var = tk.StringVar()
summoner_var = tk.StringVar()
summoner_names_var = tk.StringVar()

# Create the entry widgets and associate with the StringVars
limit_entry = tk.Entry(root, textvariable=limit_var)
summoner_entry = tk.Entry(root, textvariable=summoner_var)
summoner_names_entry = tk.Entry(root, textvariable=summoner_names_var)

# Create labels
limit_label = tk.Label(root, text="Limit:")
summoner_label = tk.Label(root, text="Summoner Name:")
summoner_names_label = tk.Label(root, text="Summoner Names (comma-separated):")
table_label = tk.Label(root, text="Results:")

# Create a button to trigger the search
search_button = tk.Button(root, text="Search", command=search_matches)

# Create a label to display the win rate
win_rate_label = tk.Label(root)

# Grid layout for the widgets
limit_label.grid(row=0, column=0, sticky=tk.W)
limit_entry.grid(row=0, column=1, padx=10, pady=5)
summoner_label.grid(row=1, column=0, sticky=tk.W)
summoner_entry.grid(row=1, column=1, padx=10, pady=5)
summoner_names_label.grid(row=2, column=0, sticky=tk.W)
summoner_names_entry.grid(row=2, column=1, padx=10, pady=5)
search_button.grid(row=3, column=0, columnspan=2, pady=5)
win_rate_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
table_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Create a label to display the table
table_label = tk.Label(root)

if consolidated_details is not None:
    # Create a list to store the table data
    table_data = []

    # Iterate over the consolidated details and format the data for the table
    for match_id, match_info in consolidated_details.items():
        row = [
            f"Match {match_id}",
            match_info['game_creation'],
            'Yes' if match_info['win'] else 'No',
        ]
        for summoner_name, summoner_info in match_info['summoner_details'].items():
            row.extend([
                summoner_name,
                summoner_info['champion'],
                summoner_info['kills'],
                summoner_info['assists'],
                summoner_info['deaths'],
                summoner_info['champ_damage']
            ])
        table_data.append(row)

    # Format the table using tabulate
    table = tabulate(table_data, headers=["Match ID", "Game Creation", "Win", "Summoner Name", "Champion", "Kills", "Assists", "Deaths", "Champion Damage"], tablefmt="pretty")
    table_label.config(text=table)
    table_label.pack()

# Start the Tkinter event loop
root.mainloop()
