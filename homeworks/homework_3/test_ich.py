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

def test_ich_page_elements(driver):
    driver.get("https://itcareerhub.de/ru")
    wait = WebDriverWait(driver, 10)

    print("\nChecking for presence of main elements on page...")

    #1. Checking the display of the ITCareerHub logo
    try:
        logo_ich = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/div/div[11]/a/img")))
        assert logo_ich.is_displayed(), "ITCareerHub logo is not displayed."
        print("Success, ITCareerHub logo found")
    except Exception as e:
        pytest.fail(f"Failed to find ITCareerHub logo: {e}")

    # 2. Checking for navigation links:(“Programs”,“Payment methods", “News", “About us”, “Reviews”)

    navigation_links = {
        "Программы": "/html/body/div[1]/div[5]/div/div/div[4]/a",
        "Способы оплаты": "/html/body/div[1]/div[5]/div/div/div[3]/a",
        "Новости": "/html/body/div[1]/div[5]/div/div/div[5]/a",
        "О нас": "/html/body/div[1]/div[5]/div/div/div[6]/a",
        "Отзывы": "/html/body/div[1]/div[5]/div/div/div[7]/a"
    }

    for link_text, xpath in navigation_links.items():
        try:
            link = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            assert link.is_displayed(), f"Link {link_text} is not displayed."
            print(f"Success, {link_text} is located")
        except Exception as e:
            pytest.fail(f"Failed to find link {link_text}: {e}")

    # 3. Checking the language switching buttons (ru and de)

    try:
        ru_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/div/div[9]/a")))
        assert ru_button.is_displayed(), "Button 'RU' is not displayed."
        print(f"Success, Button DE found")
    except Exception as e:
        pytest.fail(f"Failed to find Button: {e}")

    try:
        de_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/div/div[10]/div/a")))
        assert de_button.is_displayed(), "Button 'DE' is not displayed."
        print(f"Success, Button DE found")
    except Exception as e:
        pytest.fail(f"Failed to find Button: {e}")

    print("\n Main elements checked ✅")
    print("\nChecking the clickability of the telephone handset icon")

    # 4. Click on the icon with the telephone receiver
    try:
        phone_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[5]/div/div/div[13]/a/img")))
        phone_icon.click()
        print("Click was made.")
    except Exception as e:
        pytest.fail(f"Failed to click on the handset icon: {e}")

    # 5. Checking the text display "Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами"

    expected_text = "Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами"
    try:
        callback_elem = wait.until(EC.visibility_of_element_located((By.XPATH, f"/html/body/div[1]/div[7]/div/div[1]/div/div/div/div/div[6]/a")))
        assert callback_elem.is_displayed(), f"Text {expected_text} is not displayed."
        print(f"Success, Text: '{expected_text}' is displayed")
    except Exception as e:
        pytest.fail(f"Unable to find or verify text {expected_text}: {e}")