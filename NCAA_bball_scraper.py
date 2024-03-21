from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime, timedelta

# Setup Chrome and Selenium to ignore SSL errors
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')  # Uncomment if you don't want the browser window to open
driver = webdriver.Chrome(service=service, options=options)

# Function to scrape and save game results for a given date
def scrape_and_save(date):
    url = f'https://www.espn.com/mens-college-basketball/schedule/_/date/{date.strftime("%Y%m%d")}'
    driver.get(url)
    time.sleep(5)  # Adjust the sleep time if necessary to ensure the page loads completely
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    games = []
    for row in soup.find_all('tr', attrs={'class': 'Table__TR Table__TR--sm Table__even'}):
        cols = row.find_all('td')
        if len(cols) > 1:  # Making sure it's not an empty row
            teams_text = cols[0].text.strip()
            time_score = cols[1].text.strip()
            teams = teams_text.split(' @ ')
            if len(teams) == 2:
                team, oppTeam = teams
            else:
                team = teams[0]
                oppTeam = "TBD"
            game_info = {
                'Team': team,
                'OppTeam': oppTeam,
                'Time/Score': time_score,
            }
            games.append(game_info)
    # Save to CSV
    csv_file = f"game_results_{date.strftime('%Y%m%d')}.csv"
    csv_columns = ['Team', 'OppTeam', 'Time/Score']
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for game in games:
                writer.writerow(game)
        print(f"Data saved to {csv_file}")
    except IOError:
        print("I/O error")

# Generate and save files for the next two weeks
start_date = datetime.now()
for i in range(14):  # Next 14 days including today
    scrape_date = start_date + timedelta(days=i)
    scrape_and_save(scrape_date)

# Close the browser
driver.quit()
