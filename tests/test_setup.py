import pytest
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# Define a reusable fixture that provides URLs for test pages.
# This makes it easier to manage and change URLs from a single place.
@pytest.fixture(scope="module")
def pages_fixture():
    return {
        "orange": "https://opensource-demo.orangehrmlive.com/web/index.php",
        "google": "https://www.google.com/",
    }


class TestSetup:
    # This fixture is automatically used for the entire test class (scope="class", autouse=True)
    # It is responsible for setting up and tearing down the Selenium WebDriver for browser automation.
    @pytest.fixture(scope="class", autouse=True)
    def setup(self, request):
        session = requests.Session()
        request.cls.session = session
        # Set Chrome options for headless mode (for CI)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Initialize the Chrome WebDriver instance
        driver = webdriver.Chrome(options=options)
        # Maximize the browser window for better visibility during tests
        driver.maximize_window()
        # Attach the driver to the class instance (e.g., self.driver)
        request.cls.driver = driver
        # Yield control to the test(s); test methods will execute after this point
        yield
        # After all tests in the class have run, quit the browser and clean up resources
        driver.quit()
        # Also close the requests session after all tests are done
        session.close()
