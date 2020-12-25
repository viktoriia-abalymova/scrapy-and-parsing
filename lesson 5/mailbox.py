from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint


chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://account.mail.ru/')

elem = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, 'username'))
)
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

elem = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, 'password'))
)
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)

first_letter = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'llc__container'))
)

if first_letter:
    first_letter.click()

    mails_list = []
    count = 0
    while True:
        letter = {}
        author = driver.find_element_by_xpath(".//div[@class='letter__author']").get_attribute('title')
        recipient = driver.find_element_by_xpath(".//span[@class='letter-contact']").get_attribute('title')
        date = driver.find_element_by_xpath(".//div[@class='letter__date']")
        body = driver.find_element_by_xpath(".//div[@class='letter__body']")

        letter['author'] = author
        letter['recipient'] = recipient
        letter['date'] = date
        letter['body'] = body

        mails_list.append(letter)
        count += 1

        try:
            driver.find_element_by_xpath("//span[contains(@class,'button2_arrow-down')]").click()
        except Exception:
            break

pprint(mails_list)
pprint(f'Количество писем: {count}')
driver.close()