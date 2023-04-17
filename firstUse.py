from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

driver = webdriver.Chrome()
driver.get("https://ezamowienia.gov.pl/mo-client-board/bzp/list")
time.sleep(2)
elem = driver.find_element(by=By.CLASS_NAME, value="btn-link")
elem.click()
time.sleep(2)
elem2 = driver.find_element(by=By.ID, value="lib-date-0")
elem2.click()
time.sleep(2)
elem2 = driver.find_element(by=By.PARTIAL_LINK_TEXT, value='aria-label="2023-03-03"')
elem2.click()
time.sleep(2)
elem3 = driver.find_element(by=By.ID, value="lib-date-1")
elem3.click()
time.sleep(10)

driver.close()
