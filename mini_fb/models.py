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
    
    def get_status_messages(self):
        '''Returns a QuerySet of all Status Messages by this Profile
        '''
        # Use the ORM to retrieve StatusMessages for which the FK is this Profile
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
class StatusMessage(models.Model):
    ''' Models the data attribute of a Facebook-like status message
    '''

    # data attributes of a StatusMessage
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)

    def __str__(self):
        ''' Returns a string representation of this StatusMessage
        '''
        return f'Status Message by {self.profile.first_name} {self.profile.last_name} on {self.timestamp}'