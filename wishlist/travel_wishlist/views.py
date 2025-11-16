from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
# decorator to require login for certain views

# Create your views here.

# Create a view to show the list of places
# filter only unvisited places and order them by name
@login_required     # uses the login_required decorator from above
def place_list(request):

    # Handle the form submission
    # if the request method is POST, we need to process the form data
    # create a NewPlaceForm instance with the POST data
    # if the form is valid, save the new place to the database
    # then redirect to the place_list view to show the updated list
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save()
        if form.is_valid():
            form.save()
            return redirect('place_list')

    # if not a POST request, just show the list of unvisited places
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places})

# Create a view to show the list of visited places
@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': places_visited})

# Create a view to mark a place as visited
@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect('place_list')

# Notice place_pk argument - Django provides this argument when the
# URL is resolved. If the request is to /place/10/was_visited, then place_pk will be 10
# If this is a POST request, find the place with this pk, change visited to True, and save
# Redirect to place_list to show the wishlist