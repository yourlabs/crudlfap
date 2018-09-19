"""Test Cases."""
import time

from login_test_case import LoginTestCase

from selenium.webdriver.common.keys import Keys


class SignInTestCase(LoginTestCase):
    """This class manage login test case."""

    def test_signin(self):
        """Check system login feature."""
        if self.test_login():
            assert 'Log out' in self.driver.page_source


class CreateArtistTestCase(LoginTestCase):
    """This class manage create artist test case."""

    def test_create_artist(self):
        """This method manage the proccess of create artist step by step."""

        login = self.test_login()
        print("Login: ", login)
        if login:
            time.sleep(1)
            self.driver.find_element_by_class_name('sidenav-trigger').click()
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[3]/a').click()
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[3]/div/ul/li[1]/a').click()

            name = self.driver.find_element_by_id('id_name')
            submit = self.driver.find_element_by_xpath(
                '//*[@id="form-object-artist"]/div[2]/button')

            name.send_keys('scottlat-mahendra')
            submit.send_keys(Keys.RETURN)
            time.sleep(1)
            # check the returned result
            assert 'scottlat' in self.driver.page_source
            print("artist created")


class SearchArtistCase(LoginTestCase):
    """This class manage create artist test case."""

    def test_search_artist(self):
        """This method manage the proccess of create song step by step"""

        login = self.test_login()
        if login:
            time.sleep(1)
            self.driver.find_element_by_class_name('sidenav-trigger').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[3]/a').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[3]/div/ul/li[2]/a').click()
            time.sleep(1)
            search = self.driver.find_element_by_id('id_q')
            search.send_keys('sccot')
            time.sleep(1)
            # check the returned result
            assert 'sccot' in self.driver.page_source
            print("artist searched")


class UpdateArtistListCase(LoginTestCase):
    """This class manage update artist test case."""

    def test_update_artist_list(self):
        """This method manage the proccess of update artist step by step"""

        login = self.test_login()
        if login:
            time.sleep(1)
            self.driver.find_element_by_class_name('sidenav-trigger').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[3]/a').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[3]/div/ul/li[2]/a').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="render-table"]/div/div/div/table/tbody/tr/td[3]/a').click()  # noqa
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="row-actions-12"]/li[2]/a').click()
            time.sleep(1)
            update = self.driver.find_element_by_id('id_name')
            time.sleep(1)
            submit = self.driver.find_element_by_xpath(
                '//*[@id="form-object-artist"]/div[2]/button')
            time.sleep(1)
            update.send_keys(' john')
            submit.send_keys(Keys.RETURN)
            time.sleep(1)
            # check the returned result
            assert ' john' in self.driver.page_source
            print("Updated Artist information")
