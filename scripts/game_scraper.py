import sys
from datetime import datetime, timedelta
import pandas as pd
import os

# Adjust the path to the directory containing your package
sys.path.append(r"C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\CBBpy-master\src")
from cbbpy import mens_scraper

def clean_team_name(team_name):
    """
    Cleans the team name by removing the mascot name, which is the last word.
    """
    team_name_parts = team_name.split(' ')[:-1]
    cleaned_name = ' '.join(team_name_parts)
    return cleaned_name

def main():
    # Ensure the output directory exists
    output_dir = r"C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Results\game_results"
    os.makedirs(output_dir, exist_ok=True)

    # Loop for 7 days starting from yesterday
    for i in range(-1, 6):
        specific_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        game_ids = mens_scraper.get_game_ids(specific_date)

        all_game_info = pd.DataFrame()

        for game_id in game_ids:
            game_info, _, _ = mens_scraper.get_game(game_id)
            
            # Clean the team names to remove mascots
            game_info['home_team'] = game_info['home_team'].apply(clean_team_name)
            game_info['away_team'] = game_info['away_team'].apply(clean_team_name)
            
            # Select and rename the columns you need from game_info
            game_info_renamed = game_info[['home_team', 'home_score', 'away_team', 'away_score']].rename(columns={
                'home_team': 'Team',
                'home_score': 'TeamScore',
                'away_team': 'OppTeam',
                'away_score': 'OppScore'
            })
            
            # Add a date column to game_info_renamed
            game_info_renamed['Date'] = specific_date
            
            # Append this game's info to the all_game_info DataFrame
            all_game_info = pd.concat([all_game_info, game_info_renamed], ignore_index=True)

        # Define the output file name based on the specific date
        output_file_name = f"game_results_{specific_date}.csv"
        output_path = os.path.join(output_dir, output_file_name)

        # Save the all_game_info DataFrame to a single CSV file
        all_game_info.to_csv(output_path, index=False)
        print(f"Saved compiled game info for {specific_date} to {output_path}")

if __name__ == "__main__":
    main()
