from datetime import date
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import formats
from selenium import webdriver


class HomeNewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def get_full_url(self, namespace):
        return "{0}{1}".format(self.live_server_url, reverse(namespace))

    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("Alert", self.browser.title)

    def test_h2_css(self):
        self.browser.get(self.get_full_url("home"))
        h2 = self.browser.find_element_by_tag_name("h2")
        self.assertIn(h2.value_of_css_property(
            "color"), "rgba(0, 0, 0, 1)")

    def test_home_files(self):
        self.browser.get(self.live_server_url + "/robots.txt")
        self.assertNotIn("Not Found", self.browser.title)
        self.browser.get(self.live_server_url + "/humans.txt")
        self.assertNotIn("Not Found", self.browser.title)
