# Assignment 4 - Child Nodes Using CSS
# parent child  -> any element inside the parent
# parent > child -> only the direct child, one level down

import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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

    # the button sitting inside div class="mouse-hover"
    hover_button = driver.find_element(By.CSS_SELECTOR, "div.mouse-hover > button#mousehover")
    print("Button inside div.mouse-hover:", hover_button.text)

    # space means any depth, > means direct child only
    inside_checkbox_div = driver.find_elements(By.CSS_SELECTOR, "div#checkbox-example input")
    direct_children = driver.find_elements(By.CSS_SELECTOR, "div#checkbox-example > input")
    print("div#checkbox-example input   ->", len(inside_checkbox_div), "(inputs are deeper inside a fieldset)")
    print("div#checkbox-example > input ->", len(direct_children), "(nothing, because they are not direct children)")

    # full path from the div down to the input
    option3 = driver.find_element(By.CSS_SELECTOR, "div#checkbox-example > fieldset > label > input[value='option3']")
    option3.click()
    print("Clicked option3 through the full parent path, selected:", option3.is_selected())

    radio2 = driver.find_element(By.CSS_SELECTOR, "#radio-btn-example fieldset > label > input[value='radio2']")
    radio2.click()
    print("Clicked radio2 inside #radio-btn-example, selected:", radio2.is_selected())

    # nth-child picks one child out of a group of same tags
    second_option = driver.find_element(By.CSS_SELECTOR, "select#dropdown-class-example > option:nth-child(2)")
    second_option.click()
    print("Picked the 2nd option of the dropdown:", second_option.text)

    header_cells = driver.find_elements(By.CSS_SELECTOR, "table.table-display > tbody > tr:nth-child(1) > th")
    print("Table headers:", [cell.text for cell in header_cells])

    first_course = driver.find_element(By.CSS_SELECTOR, "table.table-display > tbody > tr:nth-child(2) > td:nth-child(2)")
    print("First course name:", first_course.text)

    # li > a misses the first one because that link sits inside an h3
    direct_links = driver.find_elements(By.CSS_SELECTOR, "#gf-BIG td:nth-child(1) ul > li > a")
    all_links = driver.find_elements(By.CSS_SELECTOR, "#gf-BIG td:nth-child(1) ul li a")
    print("Footer column with li > a :", [link.text for link in direct_links])
    print("Footer column with li a   :", [link.text for link in all_links])

    # hover on the button so the hidden links inside the same div show up
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hover_button)
    ActionChains(driver).move_to_element(hover_button).perform()
    hidden_links = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.mouse-hover-content > a"))
    )
    print("Links revealed on hover:", [link.text for link in hidden_links])

    assert hover_button.text == "Mouse Hover"
    assert len(inside_checkbox_div) == 3 and len(direct_children) == 0
    assert option3.is_selected()
    assert radio2.is_selected()
    assert header_cells[0].text == "Instructor"
    assert len(all_links) > len(direct_links)
    assert len(hidden_links) == 2
    print("\nAssignment 4 done")

finally:
    driver.quit()
