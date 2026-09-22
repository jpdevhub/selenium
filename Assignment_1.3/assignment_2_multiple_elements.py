# Assignment 2 - Multiple Element Identification
# find_elements gives a list, so we can loop over all links and print their text

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

try:
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.ID, "checkbox-example")))
    print("Page title:", driver.title)

    links = driver.find_elements(By.TAG_NAME, "a")
    print("\nTotal links on the page:", len(links))
    for i, link in enumerate(links, start=1):
        text = link.text.strip()
        print(i, "->", text if text else "(no text)")

    # searching inside one element instead of the whole page
    footer = driver.find_element(By.ID, "gf-BIG")
    footer_links = footer.find_elements(By.TAG_NAME, "a")
    print("\nLinks inside the footer:", len(footer_links))

    first_column = footer.find_elements(By.TAG_NAME, "td")[0]
    column_links = first_column.find_elements(By.TAG_NAME, "a")
    print("Links in the first footer column:", len(column_links))
    for link in column_links:
        print(" ", link.text, "->", link.get_attribute("href"))

    checkboxes = driver.find_elements(By.CSS_SELECTOR, "#checkbox-example input[type='checkbox']")
    print("\nCheckboxes found:", len(checkboxes))
    for box in checkboxes:
        print(" ", box.get_attribute("value"), "selected:", box.is_selected())

    for box in checkboxes:
        if box.get_attribute("value") == "option2":
            box.click()
            print("Clicked option2, selected now:", box.is_selected())

    rows = driver.find_elements(By.CSS_SELECTOR, "table[name='courses'] tr")
    print("\nRows in the courses table:", len(rows))
    for row in rows[1:4]:
        cells = row.find_elements(By.TAG_NAME, "td")
        print(" ", " | ".join(cell.text for cell in cells))

    assert len(links) > 1
    assert len(footer_links) < len(links)
    assert len(checkboxes) == 3
    assert checkboxes[1].is_selected()
    print("\nAssignment 2 done")

finally:
    driver.quit()
