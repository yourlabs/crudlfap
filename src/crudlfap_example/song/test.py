"""Test cases for song applcation."""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from login_test_case import LoginTestCase
import os


class CreateSongs(LoginTestCase):
    """This class manage create song test case."""
    
    
    def test_create_song(self):
        """This method manage the proccess of create song step by step"""
        self.setUp(name="Create Song")
        
        login = self.test_login()
        """This method will check user logged in or not."""
        print("login :", login)
        if login:
            self.driver.find_element_by_class_name('sidenav-trigger').click()
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[4]').click()
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[4]/div/ul/li[1]').click()

            time.sleep(1)
            self.driver.execute_script(
                "document.getElementById('id_artist').style.display = 'block'")
            self.driver.execute_script(
                "document.getElementById('id_owner').style.display = 'block'")
            artist = self.driver.find_element_by_id('id_artist')
            title = self.driver.find_element_by_id('id_name')
            duration = self.driver.find_element_by_id('id_duration')
            owner = self.driver.find_element_by_id('id_owner')

            submit = self.driver.find_element_by_xpath(
                '//*[@id="form-object-song"]/div[2]/button')

            artist.send_keys('Test')
            title.send_keys('songs for all')
            duration.send_keys('360')
            owner.send_keys('admin')

            # submitting the form
            submit.send_keys(Keys.RETURN)
            time.sleep(1)
            # check the returned result
            assert 'Test' in self.driver.page_source


class SearchSongCase(LoginTestCase):
    """This class manage search song test case."""

    def test_search_song(self):
        """This method manage the proccess of search song step by step"""

        login = self.test_login()
        """This method will check user logged in or not."""
        if login:
            time.sleep(1)
            self.driver.find_element_by_class_name('sidenav-trigger').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[4]/a').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="slide-out"]/li[2]/ul/li[4]/div/ul/li[2]/a').click()
            time.sleep(1)
            search = self.driver.find_element_by_id('id_q')
            search.send_keys('forever')
            time.sleep(1)
            # check the returned result
            assert 'test1' in self.driver.page_source
            print("song searched")


class DeleteSongCase(LoginTestCase):
    """This class manage delete song test case."""

    def test_delete_song(self):
        """This method manage the proccess of delete song step by step"""

        login = self.test_login()
        """This method will check user logged in or not."""
        if login:
            time.sleep(1)
            driver.find_element_by_class_name('sidenav-trigger').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="slide-out"]/li[2]/ul/li[4]/a').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="slide-out"]/li[2]/ul/li[4]/div/ul/li[2]/a').click()
            time.sleep(1)
            driver.find_element_by_class_name('even').find_element_by_class_name('dropdown-trigger').click()
            time.sleep(1)

            driver.find_element_by_class_name('even').find_element_by_tag_name('li').click()
            time.sleep(1)
            delete = driver.find_element_by_id('modal').find_element_by_id('main-form').find_element_by_class_name('modal-footer').find_element_by_tag_name('button').click()

            #check the returned result
            # assert '' in driver.page_source
            print("song deleted")
