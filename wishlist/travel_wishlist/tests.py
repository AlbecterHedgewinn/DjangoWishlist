from django.test import TestCase
from django.urls import reverse
# reverse is used to get the URL for a given view name

from .models import Place

# Create your tests here.

class TestHomePage(TestCase):

    def test_load_home_page_shows_empty_wishlist_for_empty_db(self):
        homepage_url = reverse('place_list')
        response = self.client.get(homepage_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist.')

class TestWishList(TestCase):

    fixtures = ['test_places']
    # load the test_places.json fixture before running the tests

    def test_view_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')


#Write a test that checks that the visited page has a "You have not visited any places yet." message
class TestNotVisited(TestCase):
    def test_view_visited_places_shows_no_visited_message_for_empty_db(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet.')


# Test visited places – and only visited places - are displayed
# create a new test class
# • Load the test_places.json fixtures file
# • Test the visited places (Moab, San Francisco) are displayed, and the not visited places (Tokyo, New York) are not
class TestVisitedPlaces(TestCase):

    fixtures = ['test_places']

    def test_view_visited_places_contains_only_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')

        self.assertContains(response, 'Moab')
        self.assertContains(response, 'San Francisco')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')