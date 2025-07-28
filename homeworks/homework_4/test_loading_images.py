import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture(scope="module")
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_alt_attribute_third_image(driver):
    url = "https://bonigarcia.dev/selenium-webdriver-java/loading-images.html"
    expected_value = "award"
    expected_image_amount = 4

    try:
        driver.get(url)
        print(f"\n🌐 Go to the Loading Images website {url}.")
    except Exception as e:
        pytest.fail(f"Failed to load {url}: {e}")

    wait = WebDriverWait(driver, 50)

    images = []
    try:
        wait.until(
            lambda d: len(d.find_elements(By.TAG_NAME, "img")) > expected_image_amount,
            message=f"Failed to find at least {expected_image_amount} images ot the page."
        )
        images = driver.find_elements(By.TAG_NAME, "img")
    except Exception as e:
        pytest.fail(f"Problem waiting for images to appear in DOM: {e}")

    try:
        for i, img in enumerate(images):
            wait.until(
                lambda d, image=img: image.get_attribute("naturalWidth") is not None and\
                                     int(image.get_attribute("naturalWidth")) > 0 and\
                                     image.get_attribute("naturalHeight") is not None and
                                     int(image.get_attribute("naturalHeight")) > 0,
                message=f"Image #{i + 1} did not load completely within the allotted time."
            )
    except Exception as e:
        pytest.fail(f"Problem waiting for images to fully load: {e}")

    if len(images) < expected_image_amount:
        pytest.fail(f"Failed of loading. Expected {expected_image_amount} images but got {len(images)}")

    print("Checking 'alt' attribute of the third image...")

    actual_alt_value = ""
    try:
        third_image = images[expected_image_amount-1]
        actual_alt_value = third_image.get_attribute("alt")
        print(f"✅  Success, got alt value '{actual_alt_value}' at the third_image.")
    except IndexError:
        pytest.fail(f"The list of images empty or or contains less than {expected_image_amount} elements.")
    except Exception as e:
        pytest.fail(f"Failed to get the attribute 'alt' from the third image:: {e}")

    try:
        assert actual_alt_value == expected_value, f"Expected '{expected_value}' but got '{actual_alt_value}'"
    except AssertionError as e:
        pytest.fail(e.args[0])