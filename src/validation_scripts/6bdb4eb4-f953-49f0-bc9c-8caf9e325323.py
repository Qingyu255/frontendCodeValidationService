import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sys
import time

if os.environ.get("ENVIRONMENT") is not None and os.environ.get("ENVIRONMENT").lower() == "dev":
    chromeOptions = Options()
    chromeOptions.add_argument("--headless=new")
    driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=chromeOptions)
else:
    # prod settings for docker container
    service = Service("/usr/bin/chromedriver")
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chromeOptions)

port = sys.argv[1]

try:
    # Open the webpage using the port number provided
    driver.get(f"http://127.0.0.1:{port}")

    passedAssertions = 0
    totalAssertions = 3

    # Verify initial state of the color box
    color_box = driver.find_element(By.ID, 'colorBox')
    change_color_button = driver.find_element(By.ID, 'changeColorButton')

    assert color_box.value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)', "Initial color box background color should be red"
    print("PASS: Initial color box background color is red.--")
    passedAssertions += 1

    # Change the color and verify the color box updates
    initial_color = color_box.value_of_css_property('background-color')
    change_color_button.click()
    time.sleep(0.5)
    new_color = color_box.value_of_css_property('background-color')

    assert new_color != initial_color, "Color box background color should change after clicking the button"
    print("PASS: Color box background color changed.--")
    passedAssertions += 1

    # Change the color again and verify the color box updates
    change_color_button.click()
    time.sleep(0.5)
    another_new_color = color_box.value_of_css_property('background-color')

    assert another_new_color != new_color, "Color box background color should change again after clicking the button"
    print("PASS: Color box background color changed again.--")
    passedAssertions += 1

    if passedAssertions == totalAssertions:
        print("Correct Answer: All tests passed!")

except AssertionError as e:
    print(f"Incorrect Answer: {passedAssertions} out of {totalAssertions} tests passed")
    raise e
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
    raise e
finally:
    driver.quit()
