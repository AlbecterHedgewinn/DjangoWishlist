from django.urls import path
from . import views
# these are the URL patterns for the travel_wishlist app

# we want the root URL of this app to go to the place_list view
# this will be how we see the list of places in the browser
# also add a url for places the user has visited
urlPatterns = [
    path('', views.place_list, name='place_list'),
    path('visited/', views.places_visited, name='places_visited'),
    path('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited'),
    # this is a dynamic url that takes a place's primary key as an argument
]