from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

import time


def searching_date(noticeNumber):
    driver = webdriver.Chrome()
    driver.get("https://ezamowienia.gov.pl/mo-client-board/bzp/list")
    time.sleep(2)
    more_button = driver.find_element(by=By.CLASS_NAME, value="btn-link")
    more_button.click()
    time.sleep(2)
    # posting notice number from db on website
    text_box = driver.find_element(by=By.ID, value="app-text-2")
    text_box.clear()
    text_box.send_keys(noticeNumber)
    time.sleep(2)

    search_button = driver.find_element(by=By.CLASS_NAME, value="btn-block")
    search_button.click()
    time.sleep(2)

    while True:
        x = input("Do you want to close a program? Y/N ").upper()
        if x == "Y":
            driver.close()
            break
