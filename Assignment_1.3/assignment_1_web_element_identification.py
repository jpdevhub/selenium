# Assignment 1 - Web Element Identification
# Locate elements using By.ID, By.NAME, By.TAG_NAME, By.LINK_TEXT and By.CLASS_NAME

import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://rahulshettyacademy.com/locatorspractice/"

options = webdriver.ChromeOptions()
if os.getenv("HEADLESS") == "1":
    options.add_argument("--headless=new")
options.add_argument("--window-size=1400,900")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 15)

try:
    driver.get(url)
    print("Page title:", driver.title)

    # id="inputUsername"
    username = wait.until(EC.visibility_of_element_located((By.ID, "inputUsername")))
    username.send_keys("rahulshettyacademy")
    print("By.ID -> username box found, placeholder:", username.get_attribute("placeholder"))

    # this box has no id, only name="inputPassword"
    password = driver.find_element(By.NAME, "inputPassword")
    password.send_keys("learning")
    print("By.NAME -> password box found, type:", password.get_attribute("type"))

    # returns the first h1 on the page
    heading = driver.find_element(By.TAG_NAME, "h1")
    print("By.TAG_NAME -> h1 text:", heading.text)

    # class is "submit signInBtn", class name locator takes only one word
    sign_in = driver.find_element(By.CLASS_NAME, "signInBtn")
    print("By.CLASS_NAME -> button text:", sign_in.text)

    # link text has to match exactly
    forgot = driver.find_element(By.LINK_TEXT, "Forgot your password?")
    print("By.LINK_TEXT -> link text:", forgot.text)

    # wrong password on purpose so the error message comes up
    sign_in.click()
    error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.error")))
    print("Error message:", error.text.strip())

    driver.find_element(By.LINK_TEXT, "Forgot your password?").click()
    reset_form = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='Forgot password']")))
    print("Opened form:", reset_form.text)

    assert username.get_attribute("id") == "inputUsername"
    assert password.get_attribute("name") == "inputPassword"
    assert heading.text == "Sign in"
    assert sign_in.text.lower() == "sign in"
    assert forgot.text == "Forgot your password?"
    print("All 5 locators worked")

finally:
    driver.quit()
