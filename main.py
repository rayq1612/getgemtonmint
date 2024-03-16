import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import telebot
from telebot import types

bot = telebot.TeleBot('7040853754:AAG2YBTfn98QJ6sgqYQzrH0X4_8og5aghZs')
price = 0.3

def start_browser(link):
    WINDOW_SIZE = "1920,1080"

    browser_options = Options()
    browser_options.add_argument('-headless')
    driver = webdriver.Firefox(options=browser_options)
    driver.get(link)
    time.sleep(15)
    parsing_price(driver=driver)
    print('Driver started')

def parsing_price(driver):
    # try:
        i = 3
        for element in driver.find_elements(By.CLASS_NAME, "CryptoPrice__inner"):
            for sub_element in element.find_elements(By.CLASS_NAME, "CryptoPrice__amount"):
                value = sub_element.text
                i -= 1
                if i <= 0:
                    value = value.replace(',', '.')
                    if float(value) <= price:
                        send_notification(driver.current_url, value)
                        print('Message sended')
                    else:
                        driver.refresh()
                        print('No such nfts')
                        time.sleep(2)
                        parsing_price(driver)
    
    # finally:
    #     parsing_price(driver)


def send_notification(current_url, value):
    bot.send_message(1131333483, f'Price: {value} \nLink: {current_url}', disable_web_page_preview=True)

def get_html(link: str):
    html = requests.post(link).text
    find_prices(html)

def prettify_soup(_soup):
    print(_soup.prettify())

def find_prices(html):
    _soup = BeautifulSoup(html, 'html.parser')
    print(_soup.prettify())
    for price in  _soup.find_all("div", class_="CryptoPrice__amount"):
        print(price + 1)


if __name__ == "__main__":
    pass
    start_browser('https://getgems.io/notcoin?filter=%7B%22saleType%22%3A%22fix_price%22%7D')