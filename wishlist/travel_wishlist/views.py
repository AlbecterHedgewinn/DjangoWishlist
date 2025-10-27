from django.shortcuts import render, redirect
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

# Create a view to show the list of places
# filter only unvisited places and order them by name
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