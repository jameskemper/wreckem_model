from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
import re
from datetime import datetime, timedelta

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=service, options=options)

# Function to clean oppteam text
def clean_oppteam(text):
    # Remove digits and extra spaces
    cleaned_text = re.sub(r"\d+", "", text).strip()
    # Further clean to remove any leading or trailing special characters
    cleaned_text = re.sub(r"^[^\w]+|[^\w]+$", "", cleaned_text)
    return cleaned_text

# Function to remove trailing "@" from oppteam
def remove_trailing_at(text):
    return text.rstrip('@').strip()

csv_file = r"C:\Users\James Kemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Results\current_games.csv"
csv_columns = ['Date', 'Team', 'OppTeam', 'Time/Score']

start_date = datetime.now() - timedelta(days=1)
end_date = datetime.now() + timedelta(weeks=1)

current_date = start_date
games = []

while current_date <= end_date:
    formatted_date = current_date.strftime("%Y%m%d")
    url = f'https://www.espn.com/mens-college-basketball/schedule/_/date/{formatted_date}'
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for row in soup.find_all('tr', attrs={'class': 'Table__TR Table__TR--sm Table__even'}):
        cols = row.find_all('td')
        if len(cols) > 0:
            team_text = cols[0].text.strip()
            oppteam_text = cols[1].text.strip()
            time_score = cols[2].text.strip()
            if ' @ ' in oppteam_text:
                oppteam_parts = oppteam_text.split(' @ ')
                team = clean_oppteam(team_text)  # Clean the team name from the first column
                oppteam = clean_oppteam(oppteam_parts[1])  # Clean the opponent team name
            else:
                team = clean_oppteam(team_text)
                oppteam = clean_oppteam(oppteam_text)
            game_info = {
                'Date': formatted_date,
                'Team': team,
                'OppTeam': oppteam,
                'Time/Score': time_score,
            }
            games.append(game_info)
    current_date += timedelta(days=1)

driver.quit()

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for game in games:
            writer.writerow(game)
    print(f"Data saved to {csv_file}")
except IOError:
    print("I/O error")
