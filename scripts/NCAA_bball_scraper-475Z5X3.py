import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

# Function to fetch the schedule text from the webpage
def fetch_schedule_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', type='application/ld+json')
    data = json.loads(script_tag.string)
    return data[0]['articleBody']

# Function to extract date, team names, and save them to a CSV file
def extract_and_save_schedule_info(schedule_text, game_pattern1, game_pattern2, schedule_file_path):
    # Find subheader containing the date
    subheader = re.search(r'March\s+(\d+)', schedule_text).group(0)
    
    # Extract day
    day = int(re.search(r'\d+', subheader).group(0))
    
    # Extract date
    date_str = f'March {day}, 2024'
    date = pd.to_datetime(date_str, format='%B %d, %Y')
    
    # Extract team names
    matches_team1 = game_pattern1.findall(schedule_text)
    team1_data = [{'Date': date, 'Team1': match[0].strip()} for match in matches_team1]

    matches_team2 = game_pattern2.findall(schedule_text)
    team2_data = [{'Team2': match.strip()} for match in matches_team2]

    # Combine team data
    combined_data = [{**team1, **team2} for team1, team2 in zip(team1_data, team2_data)]

    # Save schedule data to CSV
    df_schedule = pd.DataFrame(combined_data)
    df_schedule.to_csv(schedule_file_path, index=False, encoding='utf-8-sig')

# URL of the webpage containing the schedule
url = "https://www.sbnation.com/college-basketball/2024/3/13/24098869/march-madness-schedule-mens-2024-ncaa-tournament-dates-locations"

# Define the regex pattern to match game information
game_pattern1 = re.compile(r'No\.\s+\d+\s+([^\d/]+?)\s+vs\.\s+No\.\s+\d+\s+([^\d/]+?)(?:\s+\d+:\d+\s+[ap]\.m\. ET)?', re.IGNORECASE)
game_pattern2 = re.compile(r'vs\. No\.\s+\d+\s+([^\d]+?)\s+\d+', re.IGNORECASE)

# Path where the CSV file will be saved
schedule_file_path = r'C:\Users\jkemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\schedule.csv'

# Fetching the schedule text from the webpage
schedule_text = fetch_schedule_text(url)

# Extracting date, team names, and saving them to a CSV file
extract_and_save_schedule_info(schedule_text, game_pattern1, game_pattern2, schedule_file_path)

print("Schedule information saved to CSV file successfully.")
