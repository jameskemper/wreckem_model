import sys
from datetime import datetime, timedelta
import pandas as pd
import os

# Adjust the path to the directory containing your package
sys.path.append(r"C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\CBBpy-master\src")
from cbbpy import mens_scraper

def get_dates():
    """
    Generates a list of dates from today to 6 days into the future.
    """
    start_date = datetime.now()
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    return dates

def clean_team_name(team_name):
    """
    Cleans the team name by removing the mascot name, which is the last word.
    """
    team_name_parts = team_name.split(' ')[:-1]
    cleaned_name = ' '.join(team_name_parts)
    return cleaned_name

def main():
    dates = get_dates()
    all_game_info = pd.DataFrame()

    output_dir = r"C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Results\game_results"
    os.makedirs(output_dir, exist_ok=True)

    for date in dates:
        print(f"Processing games for date: {date}")  # Debugging print
        game_ids = mens_scraper.get_game_ids(date)
        print(f"Found game IDs: {game_ids}")  # Debugging print

        if not game_ids:
            print(f"No games found for {date}.")
            continue

        for game_id in game_ids:
            game_info, _, _ = mens_scraper.get_game(game_id)
            
            # Clean the team names to remove mascots
            game_info['home_team'] = game_info['home_team'].apply(clean_team_name)
            game_info['away_team'] = game_info['away_team'].apply(clean_team_name)
            
            # Prepare the data for aggregation
            game_info_renamed = game_info[['home_team', 'home_score', 'away_team', 'away_score']].rename(columns={
                'home_team': 'Team',
                'home_score': 'TeamScore',
                'away_team': 'OppTeam',
                'away_score': 'OppScore'
            })
            game_info_renamed['Date'] = date
            
            all_game_info = pd.concat([all_game_info, game_info_renamed], ignore_index=True)

    output_file_name = "game_results.csv"
    output_path = os.path.join(output_dir, output_file_name)
    all_game_info.to_csv(output_path, index=False)
    print(f"Saved compiled game info to {output_path}")

if __name__ == "__main__":
    main()
