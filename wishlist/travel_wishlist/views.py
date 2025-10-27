from django.shortcuts import render

# Create your views here.

# Create a view to show the list of places
def place_list(request):
    return render(request, 'travel_wishlist/wishlist.html')