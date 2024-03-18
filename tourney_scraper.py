from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Path to chromedriver (adjust as needed if not in PATH)
driver_path = 'path/to/chromedriver'

# URL of the page to scrape
url = 'https://www.ncaa.com/news/basketball-men/mml-official-bracket/2024-03-17/2024-ncaa-printable-bracket-schedule-march-madness'

# Initialize the driver and navigate to the URL
driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
driver.get(url)

# Wait for the dynamic content to load (adjust time as needed)
driver.implicitly_wait(10)

# Now that the page is loaded, you can parse the HTML content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the driver
driver.quit()

# Extract the main content similar to reader mode
# You'll need to inspect the page to find the main content container's class or id
main_content = soup.find('div', class_='main-content-class')  # This is an example; adjust based on actual content

if main_content:
    print(main_content.get_text(separator='\n', strip=True))
else:
    print("Main content not found. Please check the class or id and try again.")
