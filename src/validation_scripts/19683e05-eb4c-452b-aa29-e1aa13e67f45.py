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

    # Verify the title of the page
    assert driver.title == "Profile Card", f"Expected title 'Profile Card', but got '{driver.title}'"
    print("PASS: Title is 'Profile Card'.--")
    passedAssertions += 1

    # Verify the heading
    heading = driver.find_element(By.TAG_NAME, 'h1')
    assert heading.text == "Profile Card", f"Expected heading 'Profile Card', but got '{heading.text}'"
    print("PASS: Heading is 'Profile Card'.--")
    passedAssertions += 1

    # Verify the image
    profile_pic = driver.find_element(By.ID, 'profile-pic')
    assert profile_pic.get_attribute('src') == "https://via.placeholder.com/150", f"Expected src 'https://via.placeholder.com/150', but got '{profile_pic.get_attribute('src')}'"
    print("PASS: Profile picture src is 'https://via.placeholder.com/150'.--")
    passedAssertions += 1

    # Verify the name paragraph
    name_paragraph = driver.find_element(By.ID, 'name')
    assert name_paragraph.text == "Name: John Doe", f"Expected text 'Name: John Doe', but got '{name_paragraph.text}'"
    print("PASS: Name paragraph text is 'Name: John Doe'.--")
    passedAssertions += 1

    # Verify the bio paragraph
    bio_paragraph = driver.find_element(By.ID, 'bio')
    assert bio_paragraph.text == "Bio: Web Developer", f"Expected text 'Bio: Web Developer', but got '{bio_paragraph.text}'"
    print("PASS: Bio paragraph text is 'Bio: Web Developer'.--")
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
