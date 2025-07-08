# Import pytest for test case definition and parameterization: pytest is used to define and manage the test cases and their execution.
# Import time for temporary sleep to allow page elements to load: time is used to provide a small delay between interactions, allowing elements to load fully.
# Import Selenium's By for element location strategies, and NoSuchElementException for error handling: By is used for locating elements on the page, and NoSuchElementException handles cases where elements are not found.
# Import TestSetup for Selenium WebDriver setup, and pages_fixture for URLs: TestSetup initializes the WebDriver and sets up any necessary configurations, while pages_fixture provides the URLs for the tests.
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from tests.test_setup import TestSetup, pages_fixture
from utils.helpers import parametrize_generator


# ---------------------- #
# SUITE 1: PAGE TITLES   #
# ---------------------- #

CONFIG_FILE = "test_config.json"


class TestHomePage(TestSetup):

    @pytest.mark.ui
    @pytest.mark.parametrize(
        *parametrize_generator(CONFIG_FILE, "page_key", "expected_title")
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

    @pytest.mark.login
    @pytest.mark.parametrize(
        *parametrize_generator(CONFIG_FILE, "page_key", "expected_login_redirect")
    )
    def test_redirect_to_login(self, pages_fixture, page_key, expected_login_redirect):
        url = pages_fixture[page_key]
        self.driver.get(url)

        # Wait for the page to load
        self.driver.implicitly_wait(5)

        # For OrangeHRM: check if we are redirected to the login page
        current_url = self.driver.current_url
        is_redirected = "login" in current_url or "signin" in current_url

        # Assert that the redirection behavior matches the expected outcome
        assert (
            is_redirected == expected_login_redirect
        ), f"Redirection check failed for {url}, expected: {expected_login_redirect}, got: {is_redirected}"


# ---------------------------- #
# SUITE 2: ELEMENT PRESENCE    #
# ---------------------------- #


# This test suite checks whether a "Login" text element appears on the page
class TestElementLoginPage(TestSetup):

    @pytest.mark.ui
    @pytest.mark.login
    @pytest.mark.parametrize(
        *parametrize_generator(CONFIG_FILE, "page_key", "expected_login")
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

    @pytest.mark.login
    @pytest.mark.parametrize(
        *parametrize_generator(
            CONFIG_FILE, "page_key", "username", "password", "failed_message"
        )
    )
    def test_login_functionality(
        self, pages_fixture, page_key, username, password, failed_message
    ):
        self.driver.get(pages_fixture[page_key])

        # Wait for the page to load
        self.driver.implicitly_wait(5)

        # Find the username, password fields, and submit button
        try:
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            submit_button = self.driver.find_element(
                By.XPATH, "//button[@type='submit']"
            )
        except NoSuchElementException:
            assert (
                False
            ), "One of the elements (username, password, or submit button) was not found."

        # Enter username and password
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Click the submit button to log in
        submit_button.click()

        # Wait for the page to load after login attempt
        self.driver.implicitly_wait(2)

        # Check if the "Invalid credentials" message appears
        try:
            self.driver.find_element(By.XPATH, f"//*[text()='{failed_message}']")
            raise Exception("Login failed!")
        except NoSuchElementException:
            pass
