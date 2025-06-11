import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from tests.test_setup import TestSetup


class TestApiLocation(TestSetup):

    def setup_method(self):
        self.driver.get(
            "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        )
        self.driver.implicitly_wait(5)
        # Find the username, password fields, and submit button
        try:
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            submit_button = self.driver.find_element(
                By.XPATH, "//button[@type='submit']"
            )
        except NoSuchElementException:
            raise Exception(
                "One of the elements (username, password, or submit button) was not found."
            )

        username_field.send_keys("Admin")
        password_field.send_keys("admin123")
        submit_button.click()
        self.driver.implicitly_wait(5)

        for cookie in self.driver.get_cookies():
            self.session.cookies.set(cookie["name"], cookie["value"])

    @pytest.mark.api
    @pytest.mark.parametrize(
        "loc_id, loc_name",
        [
            (5, "Texas R&D"),
        ],
    )
    def test_api_locations(self, loc_id, loc_name):
        response = self.session.get(
            "https://opensource-demo.orangehrmlive.com/web/index.php/api/v2/dashboard/employees/locations"
        )

        assert (
            response.status_code == 200
        ), f"Expected status code 200, but got {response.status_code}"

        try:
            data = response.json()
            locations = data.get("data", {})
            locations_dict = {
                data["location"]["id"]: data["location"]["name"] for data in locations
            }
            assert locations_dict[loc_id] == loc_name, "Location name does not match"
        except ValueError:
            assert False, "Response body is not in JSON format"
