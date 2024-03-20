import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# The URL from which we're scraping data
url = "https://stats.ncaa.org/season_divisions/18221/livestream_scoreboards?utf8=%E2%9C%93&season_division_id=&game_date=03%2F25%2F2024&conference_id=0&tournament_id=&commit=Submit"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a list to store extracted data
data = []

# Placeholder for actual data extraction logic
# You'll need to inspect the webpage and adjust this part
for game in soup.find_all('div', class_='game'):  # Adjust this selector based on the actual HTML structure
    team = game.find('p', class_='team').text.strip()
    team_score = game.find('span', class_='team-score').text.strip()
    opp_team = game.find('p', class_='opp-team').text.strip()
    opp_score = game.find('span', class_='opp-score').text.strip()
    data.append([team, team_score, opp_team, opp_score])

# Construct the filename with the current date
# If you're scraping for a specific date, you can replace datetime.now() with that date
date_str = datetime.now().strftime("%m_%d_%Y")  # Formats the current date as MM_DD_YYYY
filename = f"C:\\Users\\jkemper\\OneDrive - Texas Tech University\\Git\\wreckem_model\\Data\\Results\\game_results\\game_results_{date_str}.csv"

# Write the data to a CSV file
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Team', 'Team Score', 'Opponent Team', 'Opponent Score'])  # Writing the header
    writer.writerows(data)  # Writing the data rows
