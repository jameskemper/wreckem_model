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
    cleaned_text = re.sub(r" |\d+", "", text).strip()
    return cleaned_text

# Function to remove trailing "@" from oppteam
def remove_trailing_at(text):
    return text.rstrip('@').strip()

# Updated file path
csv_file = r"C:\Users\James Kemper\OneDrive - Texas Tech University\Git\wreckem_model\Data\Results\tournament_games.csv"
csv_columns = ['Date', 'Team', 'OppTeam', 'Time/Score']

# Calculate date range
start_date = datetime.now() - timedelta(days=1)
end_date = datetime.now() + timedelta(weeks=3)

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
                oppteam_parts = [clean_oppteam(part) for part in oppteam_text.split(' @ ')]
                team = oppteam_parts[0]  # Ensure 'team' is updated correctly
                oppteam = ' @ '.join(oppteam_parts)
            else:
                team = team_text
                oppteam = clean_oppteam(oppteam_text)
            game_info = {
                'Date': formatted_date,
                'Team': team,
                'OppTeam': remove_trailing_at(oppteam),
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
