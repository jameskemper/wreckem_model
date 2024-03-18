import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Function to fetch team IDs and names
def fetch_team_ids(url):
    df = pd.read_csv(url)
    # Use 'Team' as the index and map it to 'TeamID'
    return df.set_index('Team')['TeamID'].to_dict()

# Base URL for NCAA basketball scores
base_url = "https://stats.ncaa.org/contests/livestream_scoreboards"

# URL for the team and team ID file
team_id_url = "https://raw.githubusercontent.com/jameskemper/wreckem_model/main/Data/MasterTeamSpellings.csv"

# Fetch team IDs and names
team_ids = fetch_team_ids(team_id_url)

# Function to format the game date for the URL
def format_date_for_url(date):
    return datetime.strftime(date, "%Y-%m-%d")

# Example date for scraping - adjust as needed
game_date = "2024-03-16"

# Parameters for the GET request
params = {
    "utf8": "✓",
    "season_division_id": "18221",
    "game_date": format_date_for_url(datetime.strptime(game_date, "%Y-%m-%d")),
    "conference_id": "0",
    "tournament_id": "",
    "commit": "Submit"
}

# Send GET request
response = requests.get(base_url, params=params)

# Placeholder for results
results = []

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all game entries
    games = soup.find_all('tr', id=lambda x: x and x.startswith('contest_'))
    
    for game in games:
        game_id = game['id'].split('_')[-1]
        game_time = game.find('td', rowspan="2").text.strip()
        teams = game.find_all('a', href=lambda x: x and '/teams/' in x)
        scores = game.find_all('div', id=lambda x: x and x.startswith('score_'))
        
        if len(teams) == 2 and len(scores) == 2:
            team_1_name = teams[0].text.strip()
            team_2_name = teams[1].text.strip()
            team_1_id = team_ids.get(team_1_name, "Unknown")
            team_2_id = team_ids.get(team_2_name, "Unknown")
            score_1 = scores[0].text.strip()
            score_2 = scores[1].text.strip()
            
            result = {
                'Game ID': game_id,
                'Game Time': game_time,
                'Team 1 ID': team_1_id,
                'Team 2 ID': team_2_id,
                'Team 1': team_1_name,
                'Team 2': team_2_name,
                'Score 1': score_1,
                'Score 2': score_2,
                'Date': game_date
            }
            results.append(result)
    
    # Convert results to DataFrame
    df = pd.DataFrame(results)
    
    # Save to CSV with a specified path
    filename = r"C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Results\NCAA_Basketball_Scores_{}.csv".format(game_date.replace('-', '_'))
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
else:
    print("Failed to retrieve data")
