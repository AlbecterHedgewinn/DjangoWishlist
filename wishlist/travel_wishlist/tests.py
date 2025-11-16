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

# Test for adding a new place
class TestAddNewPlace(TestCase):

    def test_add_new_invisited_place_to_wishlist(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)
        # Check that the correct template was used and the new place appears on the wishlist page
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_places = response.context['places']
        #should be 1 place in the response context
        self.assertEqual(1, len(response_places))
        tokyo_response = response_places[0]

        #expect this data to be in the database. Use get() to retrieve it
        tokyo_in_db = Place.objects.get(name='Tokyo', visited=False)

        # is data in the response the same as data in the database?
        self.assertEqual(tokyo_in_db, tokyo_response)

# test for visiting a place
class TestVisitPlace(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):

        # visist place pk 2 (New York)
        visit_place_url = reverse('place_was_visited', args=(2,)) # New York pk is 2 in the fixture
        response = self.client.post(visit_place_url, follow=True) # follow redirects

        # check correct template used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # check New York is no longer in the wishlist
        self.assertNotContains(response, 'New York')

        # is new york visited in the database?
        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

    # Test visist nonexistent place
    def test_visit_nonexistent_place(self):
        visit_place_url = reverse('place_was_visited', args=(200,)) # non-existent pk
        response = self.client.post(visit_place_url, follow=True)
        self.assertEqual(404, response.status_code) # expect 404 not found