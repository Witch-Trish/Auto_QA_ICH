from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get("https://itcareerhub.de/ru")
    sleep(5)

    payment_methods_link = driver.find_element(By.LINK_TEXT, "Способы оплаты")
    payment_methods_link.click()
    sleep(5)

    driver.save_screenshot("payment.png")

finally:
    driver.quit()