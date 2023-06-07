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
    table = tabulate(table_data, headers=["Match ID", "Creation", "Win"] + summoner_names * 6, tablefmt="pretty")
    table_label.config(text=table)

    # Clear the existing columns and headings
    for column in treeview.get_children():
        treeview.delete(column)
    treeview.heading("#0", text="Summoner Details")

    # Configure the column widths dynamically
    field_names = ["Match ID", "Creation", "Win"] + summoner_names * 6
    for i, field_name in enumerate(field_names):
        column_id = f"#{i + 1}"
        treeview.heading(column_id, text=field_name)
        treeview.column(column_id, width=100)  # Adjust the width as desired

    # Insert the data into the Treeview
    for row in table_data:
        treeview.insert("", tk.END, values=row)

# Create the Tkinter window
root = tk.Tk()

# Create the Treeview widget
treeview = ttk.Treeview(root)

# Add the initial column and heading for the Summoner Details
treeview.heading("#0", text="Summoner Details")

# Configure the column widths dynamically
field_names = ["Match ID", "Creation", "Win"]
for i, field_name in enumerate(field_names):
    column_id = f"#{i + 1}"
    treeview.heading(column_id, text=field_name)
    treeview.column(column_id, width=100)  # Adjust the width as desired

# Configure the Treeview to display data
treeview.pack()

# Start the Tkinter event loop
root.mainloop()
