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

try:
    driver.get(f"http://127.0.0.1:{port}")

    passedAssertions = 0
    totalAssertions = 3

    # Verify initial state of the form
    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    assert username_input.get_attribute('value') == '', "Initial username value should be empty"
    assert password_input.get_attribute('value') == '', "Initial password value should be empty"
    print("PASS: Initial input values are empty.--")
    passedAssertions += 1

    # Verify error message for empty username and password
    submit_button.click()
    time.sleep(0.5)

    username_error = driver.find_element(By.ID, 'usernameError')
    password_error = driver.find_element(By.ID, 'passwordError')
    form_message = driver.find_element(By.ID, 'formMessage')

    assert username_error.text == 'Username is required', f"Expected username error message, but got '{username_error.text}'"
    assert password_error.text == 'Password is required', f"Expected password error message, but got '{password_error.text}'"
    assert form_message.text == '', f"Expected no form message, but got '{form_message.text}'"
    print("PASS: Error messages displayed for empty fields.--")
    passedAssertions += 1

    # Verify form submission with valid data
    username_input.send_keys('testuser')
    password_input.send_keys('testpass')
    submit_button.click()
    time.sleep(0.5)

    assert username_error.text == '', f"Expected no username error message, but got '{username_error.text}'"
    assert password_error.text == '', f"Expected no password error message, but got '{password_error.text}'"
    assert form_message.text == 'Form submitted successfully', f"Expected success message, but got '{form_message.text}'"
    print("PASS: Form submitted successfully with valid data.--")
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
