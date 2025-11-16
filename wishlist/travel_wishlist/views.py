from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
# decorator to require login for certain views
# if a login page route is not set up, the server will give a 404 error and provide a redirect link to the login page
from django.http import HttpResponseForbidden
# This prevents unauthorized access to certain views
# if multiple users use the service, this will prevent one user from accessing another user's data
from django.contrib import messages
# This allows us to send one-time messages to the user, such as success or error messages



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
        place = form.save(commit=False) # create a Place object but don't save to the database yet
        place.user = request.user       # set the user to the currently logged-in user
        if form.is_valid():
            place.save()
            return redirect('place_list')

    # if not a POST request, just show the list of unvisited places
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places})
    # request_user is provided by Django and represents the currently logged-in user

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
        if place.user == request.user:   # ensure the place belongs to the logged-in user
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()  # return a 403 Forbidden response if the user is not authorized
    return redirect('place_list')

# Notice place_pk argument - Django provides this argument when the
# URL is resolved. If the request is to /place/10/was_visited, then place_pk will be 10
# If this is a POST request, find the place with this pk, change visited to True, and save
# Redirect to place_list to show the wishlist

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # does it belong to the logged-in user?
    if place.user != request.user:
        return HttpResponseForbidden()
    
    # if post request, process the submitted review form
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # temporary - display form errors as messages
        return redirect('place_details', place_pk=place.pk)
    
    # if get request, display the place details and review form
    # if place is visited, show the TripReviewForm. if not, no form
    else:
        if place.visited:
            form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()