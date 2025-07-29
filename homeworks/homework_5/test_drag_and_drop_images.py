import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.util import url
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService



@pytest.fixture
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get("https://www.globalsqa.com/demo-site/draganddrop/")

    try:
        consent_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent")))

        consent_btn.click()
    except TimeoutException:
        print("Cookie banner did not appear")

    yield driver
    driver.quit()


def test_drag_and_drop_images(driver):

    wait = WebDriverWait(driver, 10)

    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame")))
    driver.switch_to.frame(iframe)

    iframe_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gallery > li")))
    source_image = iframe_items[0]

    trash = driver.find_element(By.ID, "trash")

    ActionChains(driver).click_and_hold(source_image).move_to_element(trash).release().perform()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#trash > ul > li")))
    trash_images = driver.find_elements(By.CSS_SELECTOR, "#trash > ul > li")
    remaining_items = driver.find_elements(By.CSS_SELECTOR, "#gallery > li")

    assert len(trash_images) == 1, "In trash must be 1 picture"
    assert len(remaining_items) == 3, "In iframe must be left 3 pictures"