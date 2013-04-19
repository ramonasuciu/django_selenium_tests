from app.pages.utils import Utils
from app.pages.register import *


class SignUp(Utils):
    fixtures = ['users.json']

    def test_correct_data(self):
        register = Register(self.selenium, self.live_server_url)

        register.goto_page('%s%s' % (self.live_server_url, base_url + '/register/'))

        register.enter_data()
        activation_url = register.activate_account()
        register.goto_page('%s%s' % (self.live_server_url, activation_url))

        register.goto_page('%s%s' % (self.live_server_url, base_url + '/login/'))
        register.log_in('test1', 'test123')
        welcome_text = register.get_text(welcome_message)
        register.assert_text("Welcome", welcome_text)

    def test_invalid_email(self):
        register = Register(self.selenium, self.live_server_url)

        register.goto_page('%s%s' % (self.live_server_url, base_url + '/register/'))
        register.enter_data(email="aaa", error_message="Enter a valid e-mail address.")

    def test_existing_username(self):
        register = Register(self.selenium, self.live_server_url)

        register.goto_page('%s%s' % (self.live_server_url, base_url + '/register/'))
        register.enter_data(username="foo", error_message="A user with that username already exists.")

    def test_illegal_chars(self):
        register = Register(self.selenium, self.live_server_url)

        register.goto_page('%s%s' % (self.live_server_url, base_url + '/register/'))
        register.enter_data(username="fo o",
                            error_message="This value may contain only letters"
                                          ", numbers and @/./+/-/_ characters.")

    def test_required_fields(self):
        register = Register(self.selenium, self.live_server_url)

        register.goto_page('%s%s' % (self.live_server_url, base_url + '/register/'))
        register.enter_data(username="", email="", password1="",
                            password2="",
                            error_message="This field is required.")
        register.assert_count(error_message_locator, 4)

    def test_password(self):
        register = Register(self.selenium, self.live_server_url)

        register.goto_page('%s%s' % (self.live_server_url, base_url + '/register/'))

        # Append the below values in the password field
        # and verify that the correct message is shown each time new chars are added.
        password_data = [
            {'value': 'tes', 'strength': 'Short'},
            {'value': 't', 'strength': 'Weak'},
            {'value': '_1', 'strength': 'Good'},
            {'value': 'A', 'strength': 'Strong'},
        ]

        for i in password_data:
            register.fill_in(password1_locator, i['value'])
            message_js = register.get_text(password_message_locator)
            register.assert_equal(message_js, i['strength'])
