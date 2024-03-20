import requests
from bs4 import BeautifulSoup
import csv

# The URL from which we're scraping data
url = "https://stats.ncaa.org/season_divisions/18221/livestream_scoreboards?utf8=%E2%9C%93&season_division_id=&game_date=03%2F25%2F2024&conference_id=0&tournament_id=&commit=Submit"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a list to store extracted data
data = []

# Assuming the structure of the page and the data you want, you'll need to adjust the selectors accordingly
# This is a placeholder loop that you'll need to customize based on the actual HTML structure
for game in soup.find_all('div', class_='game'):  # This is an example; replace with actual HTML structure
    team = game.find('p', class_='team').text.strip()
    team_score = game.find('span', class_='team-score').text.strip()
    opp_team = game.find('p', class_='opp-team').text.strip()
    opp_score = game.find('span', class_='opp-score').text.strip()
    data.append([team, team_score, opp_team, opp_score])

# Write the data to a CSV file
with open('ncaa_games.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Team', 'Team Score', 'Opponent Team', 'Opponent Score'])  # Writing the header
    writer.writerows(data)  # Writing the data rows
