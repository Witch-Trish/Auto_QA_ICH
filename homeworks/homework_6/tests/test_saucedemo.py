from homeworks.homework_6.conftest import driver
from homeworks.homework_6.pages.cart_page import CartPage
from homeworks.homework_6.pages.checkout_page import CheckoutPage
from homeworks.homework_6.pages.inventory_page import ProductsPage
from homeworks.homework_6.pages.login_page import LoginPage

from homeworks.homework_6.constants_test import (
    EXPECTED_PRICE,
    USERNAME,
    PASSWORD
)

class TestSauceDemo:
    def test_purchasing_process(self, driver):
        # 1. log in to saucedemo
        login_page = LoginPage(driver)
        login_page.login(USERNAME, PASSWORD)

        # 2. adding products
        products_page = ProductsPage(driver)
        products_page.add_item_to_cart(products_page.PRODUCT_BACKPACK)
        print("first product successfully added")
        products_page.add_item_to_cart(products_page.PRODUCT_BOLT_T_SHIRT)
        print("second product successfully added")
        products_page.add_item_to_cart(products_page.PRODUCT_ONESIE)
        print("third product successfully added")

        # 3. opening cart
        products_page.go_to_cart()
        print(f"successfully activated cart, current url:{driver.current_url}")

        # 4. checkout
        cart_page = CartPage(driver)
        cart_page.click_checkout()

        # 5. fillings data for checkout
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_your_information("Test", "User", "12345")

        # 6. getting total price
        actual_total = checkout_page.get_total_price()
        print(f"\nTotal sum is: {actual_total}")

        # 7. checking total price
        expected_total = EXPECTED_PRICE
        assert actual_total == expected_total, \
            f"Expected total sum {expected_total}, but received {actual_total}"
        # 8. end of the order
        checkout_page.click_finish()