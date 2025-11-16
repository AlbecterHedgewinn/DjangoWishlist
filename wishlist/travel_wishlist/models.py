from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Create a Place model
class Place(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)    # link to the User model, cascade means if the user is deleted, delete their places too
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        photo_str = self.photo.url if self.photo else "No Photo"
        note_str = self.notes[100:] # truncate notes to first 100 characters
        return f'{self.name}, visited? {self.visited} on {self.date_visited}. Notes: {note_str}. Photo: {photo_str}'
        # this will show the name of the place and whether or not it has been visited
        # visited? True or False
        # it will also show the date visited and the photo URL if available
