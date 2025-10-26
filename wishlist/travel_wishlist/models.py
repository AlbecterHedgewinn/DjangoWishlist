from django.db import models

# Create your models here.

# Create a Place model
class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, visited? {self.visited}'
        # this will show the name of the place and whether or not it has been visited
        # visited? True or False
