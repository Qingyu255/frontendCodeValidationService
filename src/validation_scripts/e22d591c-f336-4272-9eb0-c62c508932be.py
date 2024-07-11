import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

port = sys.argv[1]
driver = webdriver.Firefox()

try:
    # Open the webpage using the port number provided
    driver.get(f"http://127.0.0.1:{port}")

    passedAssertions = 0
    totalAssertions = 5

    # Verify header properties
    header = driver.find_element(By.TAG_NAME, 'header')
    assert header.value_of_css_property('height') == '60px', "Header height should be 60px"
    assert header.value_of_css_property('background-color') == 'rgb(204, 204, 204)', "Header background color should be #ccc"
    print("PASS: Header height and background color.--")
    passedAssertions += 1

    # Verify footer properties
    footer = driver.find_element(By.TAG_NAME, 'footer')
    assert footer.value_of_css_property('height') == '100px', "Footer height should be 100px"
    assert footer.value_of_css_property('background-color') == 'rgb(204, 204, 204)', "Footer background color should be #ccc"
    print("PASS: Footer height and background color.--")
    passedAssertions += 1

    # Verify left column properties
    left_column = driver.find_element(By.CLASS_NAME, 'left')
    assert left_column.value_of_css_property('width') == '100px', "Left column width should be 100px"
    assert left_column.value_of_css_property('background-color') == 'rgb(255, 215, 0)', "Left column background color should be #ffd700"
    print("PASS: Left column width and background color.--")
    passedAssertions += 1

    # Verify right column properties
    right_column = driver.find_element(By.CLASS_NAME, 'right')
    assert right_column.value_of_css_property('width') == '100px', "Right column width should be 100px"
    assert right_column.value_of_css_property('background-color') == 'rgb(173, 255, 47)', "Right column background color should be #adff2f"
    print("PASS: Right column width and background color.--")
    passedAssertions += 1

    # Verify center column properties
    center_column = driver.find_element(By.CLASS_NAME, 'center')
    assert center_column.value_of_css_property('flex-grow') == '1', "Center column should be fluid width"
    assert center_column.value_of_css_property('background-color') == 'rgb(135, 206, 250)', "Center column background color should be #87cefa"
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