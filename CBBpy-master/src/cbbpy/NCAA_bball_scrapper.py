from datetime import datetime, timedelta
import pandas as pd

# Function to get yesterday's date in the desired format (e.g., '2023-03-15')
def get_yesterdays_date():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

# Example usage of the get_game_ids function to fetch game IDs for yesterday
yesterdays_date = get_yesterdays_date()
game_ids = get_game_ids(yesterdays_date)

# Assuming you have a function to process game IDs and collect game results
def collect_game_results_for_date(game_ids):
    game_results = []
    for game_id in game_ids:
        game_info, boxscore, pbp = get_game(game_id)
        # Process and collect the results as needed, for example, appending to a list
        game_results.append((game_info, boxscore, pbp))
    return game_results

# Collect game results for the previous day
yesterdays_game_results = collect_game_results_for_date(game_ids)

# Example function to save the results to CSV files
def save_results_to_csv(game_results, base_path):
    for i, (game_info, boxscore, pbp) in enumerate(game_results):
        game_info.to_csv(f"{base_path}/game_info_{i}.csv", index=False)
        boxscore.to_csv(f"{base_path}/boxscore_{i}.csv", index=False)
        pbp.to_csv(f"{base_path}/pbp_{i}.csv", index=False)

# Specify the base path where you want to save the CSV files
base_path = r"C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Results\game_results"

# Save the game results of yesterday to CSV files
save_results_to_csv(yesterdays_game_results, base_path)
