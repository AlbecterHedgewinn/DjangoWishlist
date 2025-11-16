from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase

# Define a test class that uses LiveServerTestCase
# Functional tests will use Selenium to interact with the live server

class TitleTest (LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)


# To run: # python manage.py test wishlist.functional_tests.TitleTest