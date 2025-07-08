from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def search_test():
    driver = webdriver.Chrome()
    driver.get("https://duckduckgo.com/")
    WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.ID, "searchbox_input")))
    driver.find_element(By.ID, "searchbox_input").send_keys("ЫВАПРОЛkjlk", Keys.ENTER)
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "THG_yNtlhifBrJDatoUn")))
    driver.find_element(By.CLASS_NAME, "THG_yNtlhifBrJDatoUn").is_displayed()

search_test()
#123