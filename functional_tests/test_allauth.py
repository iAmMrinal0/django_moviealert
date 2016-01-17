from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class TestGoogleLogin(StaticLiveServerTestCase):

    fixtures = ["allauth_fixture"]

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)

    def tearDown(self):
        self.browser.quit()

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
            (By.ID, element_id)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
            (By.ID, element_id)))

    def get_full_url(self, namespace):
        return "{0}{1}".format(self.live_server_url, reverse(namespace))

    def user_login(self):
        import json
        with open("moviealert/fixtures/google_user.json") as f:
            credentials = json.loads(f.read())
        self.get_element_by_id("Email").send_keys(credentials["Email"])
        # self.get_button_by_id("next").click()
        self.get_element_by_id("Passwd").send_keys(credentials["Passwd"])
        for btn in ["signIn", "submit_approve_access"]:
            self.get_button_by_id(btn).click()
        return

    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        google_login = self.get_element_by_id("google_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(google_login.get_attribute("href"),
                         self.live_server_url + "/accounts/google/login")
        google_login.click()
        self.user_login()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        google_login = self.get_element_by_id("google_login")

'''def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        google_login = self.get_element_by_id("google_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(google_login.get_attribute("href"),
                         self.live_server_url + "/accounts/google/login")
        google_login.click()
        self.user_login()
        button_xpath = "//button[contains(.,'Sign Up »')]"
        self.get_element_by_id("id_email").clear()
        self.get_element_by_id("id_email").send_keys("asdfg@gmail.com")
        signup = self.browser.find_element_by_xpath(button_xpath)
        signup.click()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        google_login = self.get_element_by_id("google_login")'''
