import sys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

firefox_path = "/usr/bin/firefox"
gecko = Service("/usr/local/bin/geckodriver")

options = Options()
options.binary_location = firefox_path
options.add_argument("--headless")

driver = webdriver.Firefox(service=gecko, options=options)
#driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
if sys.argv[1]:
    game = "+".join(word.lower() for word in sys.argv[1:])
else:
    print("How to use")

driver.get(f"https://store.steampowered.com/search/?term={game}")
search = driver.find_element(By.CLASS_NAME, "discount_final_price")
print(search.text)

driver.quit()