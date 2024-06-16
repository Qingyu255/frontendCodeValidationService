from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
try:
    driver.get("http://0.0.0.0:8000")

    username_field = driver.find_element(by=By.ID, value="username")
    password_field = driver.find_element(by=By.ID, value="password")
    submit_button = driver.find_element(by=By.XPATH, value="//input[@value='Submit']")

    submit_button.click()
    username_error_field = driver.find_element(by=By.ID, value="usernameError")
    assert username_error_field.text == "Username is required"

    password_error_field = driver.find_element(by=By.ID, value="passwordError")
    assert password_error_field.text == "Password is required"
except AssertionError as e:
    raise(e)
finally:
    driver.quit()
