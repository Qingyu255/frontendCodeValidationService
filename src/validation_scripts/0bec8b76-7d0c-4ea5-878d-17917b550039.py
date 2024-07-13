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
    totalAssertions = 4

    # Verify initial state of the form
    task_input = driver.find_element(By.ID, 'taskInput')
    add_button = driver.find_element(By.ID, 'addButton')
    task_list = driver.find_element(By.ID, 'taskList')

    assert task_input.get_attribute('value') == '', "Initial task input value should be empty"
    assert add_button.is_enabled(), "Add button should be enabled initially"
    assert len(task_list.find_elements(By.TAG_NAME, 'li')) == 0, "Task list should be empty initially"
    print("PASS: Initial state of input, button, and task list is correct.--")
    passedAssertions += 1

    # Add a task and verify it appears in the list
    task_input.send_keys('Task 1')
    add_button.click()
    time.sleep(0.5)

    task_items = task_list.find_elements(By.TAG_NAME, 'li')
    assert len(task_items) == 1, "Task list should contain 1 task after adding a task"
    assert task_items[0].text.startswith('Task 1'), f"Task item text should be 'Task 1', but got '{task_items[0].text}'"
    print("PASS: Task added to the list successfully.--")
    passedAssertions += 1

    # Verify remove button is present and styled correctly
    remove_button = task_items[0].find_element(By.CLASS_NAME, 'remove-button')
    assert remove_button.is_displayed(), "Remove button should be displayed"
    assert remove_button.value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)', "Remove button background color should be red"
    assert remove_button.value_of_css_property('color') == 'rgba(255, 255, 255, 1)', "Remove button text color should be white"
    print("PASS: Remove button is present and styled correctly.--")
    passedAssertions += 1

    # Remove the task and verify the list is empty
    remove_button.click()
    time.sleep(0.5)
    assert len(task_list.find_elements(By.TAG_NAME, 'li')) == 0, "Task list should be empty after removing the task"
    print("PASS: Task removed from the list successfully.--")
    passedAssertions += 1

    if passedAssertions == totalAssertions:
        print("Correct Answer: All tests passed!")

except AssertionError as e:
    print(f"Incorrect Answer: {passedAssertions} out of {totalAssertions} tests passed")
    raise(e)
except Exception as e:
    print(f"DEBUG: An unexpected error occurred: {str(e)}")
    raise e
finally:
    driver.quit()
