import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

url = 'https://www.google.com/maps/place/City+Hotel/@-7.3253895,108.2109198,17z/data=!4m11!3m10!1s0x2e6f5737c7f0de09:0xa29318f07e0da5ba!5m2!4m1!1i2!8m2!3d-7.3253895!4d108.2131085!9m1!1b1!16s%2Fg%2F11b8v9rgb1'
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-extensions')
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--incognito')
options.add_argument('--disable-application-cache')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(3)

i = 1
reviews = []
last_height = driver.execute_script("return document.querySelector('.m6QErb.DxyBCb.kA9KIf.dS8AEf').scrollHeight")
for i in range(120):
    driver.execute_script("document.querySelector('.m6QErb.DxyBCb.kA9KIf.dS8AEf').scroll(0, document.querySelector('.m6QErb.DxyBCb.kA9KIf.dS8AEf').scrollHeight)")
    # driver.execute_script("document.querySelector('.w8nwRe.kyuRq').addEventListener(click, null)")
    # ele = driver.find_element(By.CSS_SELECTOR, '.w8nwRe kyuRq')
    #ele.click()
    time.sleep(5)
    new_height = driver.execute_script("return document.querySelector('.m6QErb.DxyBCb.kA9KIf.dS8AEf').scrollHeight")
    last_height = new_height

soup = BeautifulSoup(driver.page_source, "html.parser")
containers = soup.findAll('div', attrs = {'class': 'jftiEf'})
for container in containers:
    name = container.find('div', attrs = {'class': 'd4r55'}).find('span').text
    rating = container.find('span', attrs = {'class': 'fzvQIb'}).text
    created = container.find('span', attrs = {'class': 'xRkPPb'}).find('span').text
    review = container.find('span', attrs = {'class': 'wiI7pd'}).text
    reviews.append({'Name': name, "Rating": rating, "Created": created, "Review": review})
    
time.sleep(3)

df = pd.DataFrame(reviews)
df.to_csv('reviews-hotel-google-map.csv', index=False)
print(df)
driver.close()