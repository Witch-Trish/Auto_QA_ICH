import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture(scope="module")
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_button_text_change(driver):

    url = "http://uitestingplayground.com/textinput"
    text = "ITCH"

    # 1. Go to the Text Input website.
    print(f"\nOpening the website: {url}")
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # 2. Enter the text "ITCH" into the input field.
    try:
        text_input_field = wait.until(EC.presence_of_element_located((By.ID, "newButtonName")))
        text_input_field.clear()
        text_input_field.send_keys(text)
        print(f" Text '{text}' entered in the input field.")
    except Exception as e:
        pytest.fail(f"Failed to find or enter text in the input field:{e}")

    # 3. Click on the blue button.
    try:
        blue_button = wait.until(EC.element_to_be_clickable((By.ID, "updatingButton")))
        initial_button_text = blue_button.text
        print(f"Initial button text: '{initial_button_text}'")
        blue_button.click()
        print("Blue button is clicked.")
    except Exception as e:
        pytest.fail(f"Failed to find or click the blue button:{e}")

    # 4. Checking that the button text has changed to "ITCH".
    try:
        wait.until(EC.text_to_be_present_in_element((By.ID, "updatingButton"), text))
        final_button_text = driver.find_element(By.ID, "updatingButton").text
        assert final_button_text == text
        print(f"Success, the button text has been successfully changed to '{final_button_text}'")
    except Exception as e:
        pytest.fail(f"Button text did not change to '{text}' or was not found: {e}")