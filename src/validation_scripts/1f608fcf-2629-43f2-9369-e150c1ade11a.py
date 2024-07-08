from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
try:
    driver.get("http://0.0.0.0:8000")

    count_element = driver.find_element(By.ID, 'count')
    assert count_element.text == '0', f"Initial count should be 0, but got {count_element.text}"

    # verify CSS
    button = driver.find_element(By.ID, 'incrementButton')
    assert button.value_of_css_property('background-color') == 'rgba(0, 0, 255, 1)', "Button background color is not blue"
    assert count_element.value_of_css_property('color') == 'rgba(255, 255, 255, 1)', "Count text color is not white"

    # verify JS
    for i in range(1, 4):
        button.click()
        time.sleep(0.5)
        assert count_element.text == str(i), f"After {i} clicks, count should be {i}, but got {count_element.text}"

    print("All tests passed!")

except AssertionError as e:
    raise(e)
finally:
    driver.quit()
    print("finished running script")
