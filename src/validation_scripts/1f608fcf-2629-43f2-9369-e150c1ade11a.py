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
    driver.get(f"http://127.0.0.1:{port}")

    passedAssertions = 0
    totalAssertions = 3

    count_element = driver.find_element(By.ID, 'count')
    assert count_element.text == '0', f"Initial count should be 0, but got {count_element.text}"
    print("PASS: Initial count text is 0.--") #impt: let '--' separate the logs
    passedAssertions += 1

    # verify CSS
    button = driver.find_element(By.ID, 'incrementButton')
    assert button.value_of_css_property('background-color') == 'rgba(0, 0, 255, 1)', f"Button background color is not blue"
    print("PASS: Button background color is blue.--")
    passedAssertions += 1

    # verify JS
    for i in range(1, 4):
        button.click()
        time.sleep(0.5)
        assert count_element.text == str(i), f"After {i} clicks, count should be {i}, but got {count_element.text}"
    print("PASS: Button count text increments with clicks.--")
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
