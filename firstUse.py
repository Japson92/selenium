from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

import time


def searching_date(noticeNumber):
    driver = webdriver.Chrome()
    driver.get("https://ezamowienia.gov.pl/mo-client-board/bzp/list")
    time.sleep(2)
    elem = driver.find_element(by=By.CLASS_NAME, value="btn-link")
    elem.click()
    time.sleep(2)
    # posting notice number from db on website
    elem2 = driver.find_element(by=By.ID, value="app-text-2")
    elem2.clear()
    elem2.send_keys(noticeNumber)
    time.sleep(2)

    elem3 = driver.find_element(by=By.CLASS_NAME, value="btn-block")
    elem3.click()
    time.sleep(2)
    # elem2 = driver.find_element(By.CSS_SELECTOR, 'span.flatpickr-day')
    # elem2.click()
    # time.sleep(2)
    # elem3 = driver.find_element(by=By.ID, value="lib-date-1")
    # elem3.click()
    time.sleep(10)
    while True:
        x = input("Do you want to close a program? Y/N ").upper()
        if x == "Y":
            driver.close()
            break
