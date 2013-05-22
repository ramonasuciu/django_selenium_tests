from selenium.webdriver.common.by import By
from django.core import mail
import re
import unittest


username_locator = (By.ID, "id_username")
email_locator = (By.ID, "id_email")
password_locator = (By.ID, "id_password")
password1_locator = (By.ID, "id_password1")
password2_locator = (By.ID, "id_password2")
submit_locator = (By.CSS_SELECTOR, "input[value='Submit'][type='submit']")
login_locator = (By.CSS_SELECTOR, "input[value='Log in'][type='submit']")
error_message_locator = (By.CSS_SELECTOR, "ul.errorlist li")
password_message_locator = (By.CSS_SELECTOR, ".help-inline")
account_message_locator = (By.ID, "content")
password_js = (By.CSS_SELECTOR, ".help-inline")
welcome_message = (By.CSS_SELECTOR, "h1")


class Register(unittest.TestCase):

    def __init__(self, selenium, live_server_url):
        self.selenium = selenium
        self.live_server_url = live_server_url

    def goto_page(self, url):
        self.selenium.get(url)

    def fill_in(self, locator, value):
        self.selenium.find_element(*locator).send_keys(value)

    def click_button(self, locator):
        self.selenium.find_element(*locator).click()

    def get_text(self, locator):
        return self.selenium.find_element(*locator).text

    def assert_text(self, string, text):
        assert string in text

    def assert_count(self, locator, length):
        elements = self.selenium.find_elements(*locator)
        assert len(elements) == length

    def assert_equal(self, message1, message2):
        self.assertEqual(message1, message2)

    def enter_data(self, **kwargs):
        signup_data = {
            'username': 'foo_bar',
            'email': 'foo@bar.com',
            'password1': 'test123',
            'password2': 'test123',
            'error_message': '',
        }

        signup_data.update(kwargs)

        # Enter valid signup data
        self.fill_in(username_locator, signup_data['username'])
        self.fill_in(email_locator, signup_data['email'])
        self.fill_in(password1_locator, signup_data['password1'])
        self.fill_in(password2_locator, signup_data['password2'])

        self.click_button(submit_locator)

    def activate_account(self):
        return re.search('/accounts/activate/(.*)', mail.outbox[0].body).group(0)

    def log_in(self, username, password):
        self.fill_in(username_locator, username)
        self.fill_in(password_locator, password)
        self.click_button(login_locator)
