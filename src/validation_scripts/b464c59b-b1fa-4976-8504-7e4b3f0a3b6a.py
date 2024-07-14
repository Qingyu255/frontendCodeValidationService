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
    totalAssertions = 5

    # Verify the title of the page
    assert driver.title == "Contact Us", f"Expected title 'Contact Us', but got '{driver.title}'"
    print("PASS: Title is 'Contact Us'.--")
    passedAssertions += 1

    # Verify the heading
    heading = driver.find_element(By.TAG_NAME, 'h1')
    assert heading.text == "Contact Us", f"Expected heading 'Contact Us', but got '{heading.text}'"
    print("PASS: Heading is 'Contact Us'.--")
    passedAssertions += 1

    # Verify the input fields
    name_input = driver.find_element(By.ID, 'name')
    assert name_input.get_attribute('placeholder') == "Your Name", f"Expected placeholder 'Your Name', but got '{name_input.get_attribute('placeholder')}'"
    print("PASS: Name input placeholder is 'Your Name'.--")
    passedAssertions += 1

    email_input = driver.find_element(By.ID, 'email')
    assert email_input.get_attribute('placeholder') == "Your Email", f"Expected placeholder 'Your Email', but got '{email_input.get_attribute('placeholder')}'"
    print("PASS: Email input placeholder is 'Your Email'.--")
    passedAssertions += 1

    # Verify the textarea
    message_textarea = driver.find_element(By.ID, 'message')
    assert message_textarea.get_attribute('placeholder') == "Your Message", f"Expected placeholder 'Your Message', but got '{message_textarea.get_attribute('placeholder')}'"
    print("PASS: Message textarea placeholder is 'Your Message'.--")
    passedAssertions += 1

    # Verify the submit button
    submit_button = driver.find_element(By.ID, 'submit')
    assert submit_button.text == "Send Message", f"Expected button text 'Send Message', but got '{submit_button.text}'"
    print("PASS: Submit button text is 'Send Message'.--")
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