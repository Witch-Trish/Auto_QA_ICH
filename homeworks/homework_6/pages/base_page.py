from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.base_url = "https://www.saucedemo.com/"
        self.wait = WebDriverWait(self.driver, timeout)

    def open(self, url=""):
        self.driver.get(self.base_url + url)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys_to_element(self, locator, text):
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_text_from_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator)).text