"""Selenium test cases for artist application."""
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from selenium.webdriver.chrome.options import Options
from settings import USERNAME, KEY
import unittest
import wd.parallel
import time
import copy


class LoginTestCase(LiveServerTestCase):
    """A common Login Test class to check login feature."""

    def setUp(self, name=None):
        """Setup the driver object."""
        self.desired_cap = {
            'OS': "Linux 18.04",
            'browserName': "chrome",
            'version': "latest",
        }

        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_cap,
            # command_executor="http://{0}:{1}@localhost:4445/wd/hub".format(USERNAME, KEY)
            command_executor="http://{0}:{1}@ondemand.saucelabs.com:80/wd/hub".format(USERNAME, KEY)
        )
        super(LoginTestCase, self).setUp()

    def tearDown(self):
        """Close the driver object."""
        self.driver.quit()
        super(LoginTestCase, self).tearDown()

    def test_login(self):
        """Test case for login feature."""
        driver = self.driver

        # Opening the link we want to test
        driver.get("http://127.0.0.1:8000/login")

        if "Login" not in driver.title:
            raise Exception("Unable to load login page!")

        username = driver.find_element_by_id('id_username')
        password_name = driver.find_element_by_id('id_password')
        submit = driver.find_element_by_xpath(
            '//*[@id="main-form"]/div[2]/button')
        # Fill the create user form with username and password.
        username.send_keys('admin')
        password_name.send_keys('download1')

        submit.send_keys(Keys.RETURN)
        time.sleep(1)

        # check the returned result
        if 'Log out' in driver.page_source:
            return True
        else:
            return False
