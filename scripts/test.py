import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# The URL of the page to scrape
url = "https://www.sbnation.com/college-basketball/2024/3/13/24098869/march-madness-schedule-mens-2024-ncaa-tournament-dates-locations"

# Fetch the page content
response = requests.get(url)
content = response.content

# Parse the HTML content
soup = BeautifulSoup(content, 'html.parser')

# Find the part of the page that contains the game schedule
# Assuming it starts after a specific text
schedule_marker_text = "Here is the complete schedule for March Madness 2024:"
schedule_part = soup.find(text=schedule_marker_text)

# Initialize an empty list to hold the data
data = []

# Current date placeholder
current_date = None

# Iterate through the siblings of the schedule marker, assuming they are either dates or games
for sibling in schedule_part.find_next_siblings():
    text = sibling.get_text(strip=True)
    # Check if the sibling is a date
    if ',' in text and len(text.split()) == 3:  # Simple check for a date format "Day, Month Date"
        current_date = text
    elif current_date and ('vs.' in text or ',' in text):  # Check for game information
        # Split the game information based on whether it's a future game (has 'vs.') or a past game (has a score ',')
        if 'vs.' in text:
            teams = text.split('vs.')
            team1 = teams[0].strip()
            team2 = teams[1].split(' ')[0].strip()  # Assuming the time is after the second team
        else:
            teams = text.split(',')
            team1 = teams[0].rsplit(' ', 1)[0].strip()  # Remove the score
            team2 = teams[1].split(' ', 2)[1].strip()  # Remove the score and OT if present
        # Append the data
        data.append({'date': current_date, 'team1': team1, 'team2': team2})

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df.head())

# Optional: Save the DataFrame to a CSV file
# df.to_csv('basketball_games.csv', index=False)
