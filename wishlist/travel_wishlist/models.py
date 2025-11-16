from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
# import default_storage to handle file deletions

# Create your models here.

# Create a Place model
class Place(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)    # link to the User model, cascade means if the user is deleted, delete their places too
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    # Override the save method to handle photo replacement
    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        super().save(*args, **kwargs)
        # super calls the original django save method to save the instance

    # Method to delete photo from storage
    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def __str__(self):
        photo_str = self.photo.url if self.photo else "No Photo"
        note_str = self.notes[100:] if self.notes else "No Notes" # truncate notes to first 100 characters
        return f'{self.name}, visited? {self.visited} on {self.date_visited}. Notes: {note_str}. Photo: {photo_str}'
        # this will show the name of the place and whether or not it has been visited
        # visited? True or False
        # it will also show the date visited and the photo URL if available
