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