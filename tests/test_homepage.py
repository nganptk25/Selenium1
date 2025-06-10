# Import pytest for test case definition and parameterization
# Import time for temporary sleep to allow page elements to load
# Import Selenium's By for element location strategies, and NoSuchElementException for error handling
# Import TestSetup for Selenium WebDriver setup, and pages_fixture for URLs
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from tests.test_setup import TestSetup, pages_fixture


# ---------------------- #
# SUITE 1: PAGE TITLES   #
# ---------------------- #


# This test suite verifies that the title of each homepage matches the expected string
class TestHomePageTitles(TestSetup):

    @pytest.mark.ui
    @pytest.mark.parametrize(
        "page_key, expected_title",  # Parameters for test case execution
        [
            ("orange", "OrangeHRM"),  # Test OrangeHRM homepage
            ("google", "Google"),  # Test Google homepage
        ],
    )
    def test_homepage_title(self, pages_fixture, page_key, expected_title):
        # Retrieve the URL from the shared fixture using the page key
        url = pages_fixture[page_key]

        # Open the target URL in the browser
        self.driver.get(url)

        # Assert that the title of the loaded page matches the expected title
        assert (
            self.driver.title == expected_title
        ), f"Expected title '{expected_title}' but got '{self.driver.title}'"


# ---------------------------- #
# SUITE 2: ELEMENT PRESENCE    #
# ---------------------------- #


# This test suite checks whether a "Login" text element appears on the page
class TestElementPresence(TestSetup):

    @pytest.mark.login
    @pytest.mark.parametrize(
        "page_key, expected_login",  # Parameters: page key and whether "Login" is expected
        [
            ("orange", True),  # Expect "Login" text on OrangeHRM homepage
            ("google", False),  # Do NOT expect "Login" text on Google homepage
        ],
    )
    def test_login_text_present(self, pages_fixture, page_key, expected_login):
        # Retrieve and open the target URL
        url = pages_fixture[page_key]
        self.driver.get(url)

        # Wait for a few seconds to ensure page content is fully loaded
        self.driver.implicitly_wait(5)

        # Attempt to find an element with exact visible text "Login"
        try:
            login_element = self.driver.find_element(By.XPATH, "//*[text()='Login']")
            is_present = login_element.is_displayed()
        except NoSuchElementException:
            # If the element is not found, treat it as not present
            is_present = False

        # Assert that the presence or absence of the "Login" element matches expectation
        assert is_present == expected_login, f"'Login' text presence mismatch on {url}"
