from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class Utils(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(Utils, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(Utils, cls).tearDownClass()
