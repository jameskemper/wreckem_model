import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

def scrape_ncaa_schedule(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator=' ')
    
    # Regex pattern to find dates and games
    date_pattern = re.compile(r'(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday),\s(March|April)\s(\d{1,2})\s\((Round\sof\s\d{2,64}|Elite\sEight|Final\sFour)\)')
    game_pattern = re.compile(r'\((\d+)\)\s([^|]+?)\svs\.\s\((\d+)\)\s([^|]+?)\s\|\s\d{1,2}:\d{2}\s[ap]\.m\.\s\|\s[A-Z]+')
    
    schedule = []
    current_date = None

    for line in text.split('\n'):
        date_match = date_pattern.search(line)
        if date_match:
            # Extract the date and convert it to a datetime object
            current_date = datetime.strptime(f"{date_match.group(2)} {date_match.group(3)}, 2024", "%B %d, %Y").strftime('%m/%d/%Y')
            continue
        
        game_match = game_pattern.search(line)
        if game_match and current_date:
            team, oppteam = game_match.group(2).strip(), game_match.group(4).strip()
            schedule.append([current_date, team, oppteam])
    
    return schedule

# URL of the NCAA schedule page
url = "https://www.ncaa.com/news/basketball-men/mml-official-bracket/2024-03-24/latest-bracket-schedule-and-scores-2024-ncaa-mens-tournament"

# Scrape the schedule
schedule = scrape_ncaa_schedule(url)


# Save the schedule to a CSV file
schedule_df = pd.DataFrame(schedule, columns=['Date', 'Team', 'OppTeam'])
schedule_df.to_csv(r'C:\Users\James Kemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\schedule.csv', index=False)

print("Schedule information saved to CSV file successfully.")