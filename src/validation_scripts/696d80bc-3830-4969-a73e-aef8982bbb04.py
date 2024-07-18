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
    driver.get(f"http://127.0.0.1:{port}")

    passedAssertions = 0
    totalAssertions = 5

    # Verify the title of the page
    assert driver.title == "My Simple HTML Page", f"Expected title 'My Simple HTML Page', but got '{driver.title}'"
    print("PASS: Title is 'My Simple HTML Page'.--")
    passedAssertions += 1

    # Verify the heading
    heading = driver.find_element(By.TAG_NAME, 'h1')
    assert heading.text == "Welcome to My Page", f"Expected heading 'Welcome to My Page', but got '{heading.text}'"
    print("PASS: Heading is 'Welcome to My Page'.--")
    passedAssertions += 1

    # Verify the paragraph
    paragraph = driver.find_element(By.TAG_NAME, 'p')
    assert paragraph.text == "This is a simple HTML page for testing purposes.", f"Expected paragraph 'This is a simple HTML page for testing purposes.', but got '{paragraph.text}'"
    print("PASS: Paragraph text is 'This is a simple HTML page for testing purposes.'.--")
    passedAssertions += 1

    # Verify the unordered list items
    list_items = driver.find_elements(By.TAG_NAME, 'li')
    expected_texts = ["Item 1", "Item 2", "Item 3"]
    for i, item in enumerate(list_items):
        assert item.text == expected_texts[i], f"Expected list item '{expected_texts[i]}', but got '{item.text}'"
        print(f"PASS: List item {i + 1} text is '{expected_texts[i]}'.--")
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
