import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

@pytest.fixture(scope="class")
def driver():
    service = ChromeService(ChromeDriverManager().install())
    options = ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()