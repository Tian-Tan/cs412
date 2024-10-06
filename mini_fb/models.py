# mini_fb/models.py
# Define the data object for our application
from django.db import models

# Create your models here.

class Profile(models.Model):
    ''' Encapsulate the idea of a user profile
    '''

    # data attributes of a Profile
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        ''' Returns a string representation of this object
        '''
        return f'{self.first_name} {self.last_name}'