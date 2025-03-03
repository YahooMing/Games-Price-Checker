import sys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



def get_price(driver, url, selector):
    """Use selenium to scrape video game prices"""
    driver.get(url)
    try:
        output = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return output.text
    except Exception:
        return "ERROR: Can't find this game on this platform"

def clean_price(price: str) -> float:
    """Change string to float"""
    return float(price.replace(" zł", "").replace(",", "."))

def compare(**kwargs):
    """Compare prices of different stores"""
    cleaned_prices = {store: clean_price(price) for store, price in kwargs.items() if price}
    if not cleaned_prices:
        return "ERROR: prices are not available"
    cheapest_store = min(cleaned_prices, key=cleaned_prices.get)
    return f"Cheapest store: {cheapest_store} - {cleaned_prices[cheapest_store]} zł"

firefox_path = "/usr/bin/firefox"
gecko = Service("/usr/local/bin/geckodriver")

options = Options()
options.binary_location = firefox_path
options.add_argument("--headless")

driver = webdriver.Firefox(service=gecko, options=options)

if sys.argv[1]:
    steam = "+".join(word.lower() for word in sys.argv[1:])
    eneba = "%20".join(word.lower() for word in sys.argv[1:])
    kinguin = eneba
else:
    print("How to use")

steam_url = f"https://store.steampowered.com/search/?term={steam}"
eneba_url = f"https://www.eneba.com/pl/store/all?drms[]=steam&enb_campaign=Main%20Search&enb_content=search%20dropdown%20-%20input&enb_medium=input&enb_source=https%3A%2F%2Fwww.eneba.com%2Fstore%2Fall&enb_term=Submit&os[]=windows&page=1&text={eneba}%20&types[]=game"
kinguin_url = f"https://www.kinguin.net/listing?platforms=2&countries=PL&active=1&hideUnavailable=0&type=kinguin&phrase={kinguin}&page=0&size=50&sort=bestseller.total,DESC"

eneba_price = get_price(driver, eneba_url, "span.L5ErLT.wTj8OK")
kinguin_price = get_price(driver, kinguin_url,"span.min[itemprop='lowPrice']" )
steam_price = get_price(driver, steam_url,"div.discount_final_price")

print(eneba_price, kinguin_price, steam_price)
print(compare(eneba=eneba_price, kinguin=kinguin_price, steam=steam_price))

driver.quit()