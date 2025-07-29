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


def test_text_presence_in_iframe(driver):
    url = "https://bonigarcia.dev/selenium-webdriver-java/iframes.html"
    target_text = "semper posuere integer et senectus justo curabitur."

    try:
        driver.get(url)
        print(f"\n\n🌐 Go to the loading website with iframe  {url}.")
    except Exception as e:
        pytest.fail(f"Failed to load {url}: {e}")


    wait = WebDriverWait(driver, 10)

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "my-iframe")))

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
    paragraphs = driver.find_elements(By.TAG_NAME,"p")

    located = False
    for index, p in enumerate(paragraphs, start=1):
        if target_text in p.text:
            assert p.is_displayed(), "Paragraph found and exist but not displayed"
            located = True
            print(f"\nThe search text '{target_text}' is located at {index} paragraph: \n\n{p.text} and displayed.")
            break
    assert located, f"The search text '{target_text}' was not found in any paragraph"