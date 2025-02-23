import sys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

firefox_path = "/usr/bin/firefox"
gecko = Service("/usr/local/bin/geckodriver")

options = Options()
options.binary_location = firefox_path
options.add_argument("--headless")

driver = webdriver.Firefox(service=gecko, options=options)
#driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
if sys.argv[1]:
    steam = "+".join(word.lower() for word in sys.argv[1:])
    eneba = "%20".join(word.lower() for word in sys.argv[1:])
else:
    print("How to use")

driver.get(f"https://store.steampowered.com/search/?term={steam}")
try:
    steam_price = driver.find_element(By.CLASS_NAME, "discount_final_price")
    print(steam_price.text)
except Exception:
    print("Can't find this game on steam")

driver.get(f"https://www.eneba.com/pl/store/all?drms[]=steam&enb_campaign=Main%20Search&enb_content=search%20dropdown%20-%20input&enb_medium=input&enb_source=https%3A%2F%2Fwww.eneba.com%2Fstore%2Fall&enb_term=Submit&os[]=windows&page=1&text={eneba}%20&types[]=game")
try:
    eneba_price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.L5ErLT.wTj8OK"))
    )
    print(eneba_price_element.text)  # Pobranie faktycznej ceny
except Exception:
    print("Can't")
driver.quit()