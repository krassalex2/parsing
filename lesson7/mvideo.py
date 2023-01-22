from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

s = Service('./chromedriver')

chromeOptions = Options()
chromeOptions.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=chromeOptions)

driver.get('https://www.mvideo.ru/')

# Ищем кнопку тренды, последовательно прокручивая страницу вниз.
trend_button = None

while True:
    actions = ActionChains(driver)
    actions.scroll_by_amount(0, 100)
    actions.perform()

    try:
        wait = WebDriverWait(driver, timeout=0.1)
        next_button = wait.until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'В тренде')]/ancestor::button")))
        next_button.click()
        break
    except:
        continue

goods_refs_items = driver.find_elements(By.XPATH, "(//mvid-product-cards-group)[2]/descendant::div[contains(@class, 'product-mini-card__name')]/div/a")
goods_prices_items = driver.find_elements(By.XPATH, "(//mvid-product-cards-group)[2]/descendant::div[contains(@class, 'product-mini-card__price')]/descendant::span[@class='price__main-value']")

goods_hrefs = [item.get_attribute('href') for item in goods_refs_items]
goods_titles = [item.text for item in goods_refs_items]
goods_prices = [item.text for item in goods_prices_items]

goods = [{'url': good[0], 'name': good[1], 'price': good[2]} for good in zip(goods_hrefs, goods_titles, goods_prices)]

client = MongoClient('localhost', 27017)
mvideo_base = client.mvideo
trends_collection = mvideo_base['trends']

for good in goods:
    trends_collection.insert_one(good)



