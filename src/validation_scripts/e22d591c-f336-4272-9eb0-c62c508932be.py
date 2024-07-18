import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import sys
import time

if os.environ.get("ENVIRONMENT") is not None and os.environ.get("ENVIRONMENT").lower() == "dev":
    chromeOptions = Options()
    chromeOptions.add_argument("--headless=new")
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chromeOptions
    )
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
    totalAssertions = 5

    # Verify header properties
    header = driver.find_element(By.TAG_NAME, 'header')
    assert header.value_of_css_property('height') == '60px', "Header height should be 60px"
    assert header.value_of_css_property('background-color') == 'rgba(204, 204, 204, 1)', "Header background color should be #ccc"
    print("PASS: Header height and background color.--")
    passedAssertions += 1

    # Verify footer properties
    footer = driver.find_element(By.TAG_NAME, 'footer')
    assert footer.value_of_css_property('height') == '100px', "Footer height should be 100px"
    assert footer.value_of_css_property('background-color') == 'rgba(204, 204, 204, 1)', "Footer background color should be #ccc"
    print("PASS: Footer height and background color.--")
    passedAssertions += 1

    # Verify left column properties
    left_column = driver.find_element(By.CLASS_NAME, 'left')
    assert left_column.value_of_css_property('width') == '100px', "Left column width should be 100px"
    assert left_column.value_of_css_property('background-color') == 'rgba(255, 215, 0, 1)', "Left column background color should be #ffd700"
    print("PASS: Left column width and background color.--")
    passedAssertions += 1

    # Verify right column properties
    right_column = driver.find_element(By.CLASS_NAME, 'right')
    assert right_column.value_of_css_property('width') == '100px', "Right column width should be 100px"
    assert right_column.value_of_css_property('background-color') == 'rgba(173, 255, 47, 1)', "Right column background color should be #adff2f"
    print("PASS: Right column width and background color.--")
    passedAssertions += 1

    # Verify center column properties
    center_column = driver.find_element(By.CLASS_NAME, 'center')
    assert center_column.value_of_css_property('flex-grow') == '1', "Center column should be fluid width"
    assert center_column.value_of_css_property('background-color') == 'rgba(135, 206, 250, 1)', "Center column background color should be #87cefa"
    print("PASS: Center column fluid width and background color.--")
    passedAssertions += 1

    # # Verify all columns have the same height
    # container = driver.find_element(By.CLASS_NAME, 'container')
    # container_height = container.value_of_css_property('height')
    # assert left_column.value_of_css_property('height') == container_height, "Left column height should match container height"
    # assert right_column.value_of_css_property('height') == container_height, "Right column height should match container height"
    # assert center_column.value_of_css_property('height') == container_height, "Center column height should match container height"
    # print("PASS: All columns have the same height.--")
    # passedAssertions += 1

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
