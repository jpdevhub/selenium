# Assignment 3 - CSS Selector Challenge
# [id^='abc'] starts with, [id$='abc'] ends with, [id*='abc'] contains
# ids here are checkBoxOption1/2/3 so [id^='checkBoxOption'] is the same idea as [id^='user_']

import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://rahulshettyacademy.com/AutomationPractice/"

options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
if os.getenv("HEADLESS") == "1":
    options.add_argument("--headless=new")
options.add_argument("--window-size=1400,900")

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(15)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 15)


def find(selector, note):
    elements = driver.find_elements(By.CSS_SELECTOR, selector)
    print("\n", selector, "->", note)
    print("   matched", len(elements))
    for element in elements:
        name = element.get_attribute("id") or element.get_attribute("name") or element.tag_name
        text = element.text.strip().replace("\n", " ")[:45]
        print("    <%s> %s %s" % (element.tag_name, name, text))
    return elements


try:
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.ID, "checkbox-example")))
    print("Page title:", driver.title)

    find("input#autocomplete", "tag with id")
    find("input.radioButton", "tag with class")
    find("input[name='radioButton'][value='radio3']", "two attributes together")

    starts_with = find("input[id^='checkBoxOption']", "id starts with checkBoxOption")
    ends_with = find("div[id$='-example']", "id ends with -example")
    contains = find("[id*='dropdown']", "id contains dropdown")

    find("input[name*='Box']", "wildcard on name instead of id")
    find("a[href$='.org/']", "href ends with .org/")
    find("*[id^='radio']", "any tag whose id starts with radio")

    for box in starts_with:
        box.click()
    print("\nTicked all three checkboxes:", [box.is_selected() for box in starts_with])

    name_box = driver.find_element(By.CSS_SELECTOR, "input[id*='name']")
    name_box.send_keys("Karan")
    print("Typed into input[id*='name'], value is:", name_box.get_attribute("value"))

    assert len(starts_with) == 3
    assert len(ends_with) == 3
    assert len(contains) == 1
    assert all(box.is_selected() for box in starts_with)
    print("\nAssignment 3 done")

finally:
    driver.quit()
