from django.urls import path
from . import views
# these are the URL patterns for the travel_wishlist app

# we want the root URL of this app to go to the place_list view
# this will be how we see the list of places in the browser
urlPatterns = [
    path('', views.place_list, name='place_list'),
]