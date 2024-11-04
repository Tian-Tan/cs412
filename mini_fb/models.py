# mini_fb/models.py
# Define the data object for our application
from django.db import models
import random
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        ''' Returns a string representation of this object
        '''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        ''' Returns a QuerySet of all Status Messages by this Profile
        '''
        # Use the ORM to retrieve StatusMessages for which the FK is this Profile
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_friends(self):
        ''' Returns a list of all Profiles who are friends with this Profile
        '''
        friends = []
        for relationship in Friend.objects.filter(profile1=self):
            friends.append(relationship.profile2)
        for relationship in Friend.objects.filter(profile2=self):
            friends.append(relationship.profile1)
        return friends
    
    def add_friend(self, other):
        ''' Creates a new Friend instance between the profiles self and other
        '''
        if (not self == other) and (not Friend.objects.filter(profile1=self, profile2=other).exists()) and (not Friend.objects.filter(profile1=other, profile2=self).exists()):
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        ''' Returns a list of 2 friend suggestions
        This is an easy algorithm to recommend 2 friends if they are not already that profile's friend
        '''
        return random.sample([profile for profile in Profile.objects.all() if (not(profile == self) and not(profile in self.get_friends()))], 2)
    
    def get_news_feed(self):
        ''' Returns the list of StatusMessages sent by the profile's friends
        '''
        feed = []
        for friend in self.get_friends():
            if StatusMessage.objects.filter(profile=friend):
                for status in StatusMessage.objects.filter(profile=friend).order_by("timestamp").reverse():
                    feed.append(status)
        print(feed)
        return feed
    
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
    
    def get_images(self):
        '''Returns a QuerySet of all Images on this StatusMessage
        '''
        # Use the ORM to retrieve Images for which the FK is this StatusMessage
        images = Image.objects.filter(status=self)
        return images
    
class Image(models.Model):
    ''' Encapsulates the idea of an image file
    '''

    # data attributes of an Image
    status = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        ''' Returns a string representation of this Image
        '''
        return f'Image of {self.status} at {self.timestamp}'
    
class Friend(models.Model):
    ''' Encapsulates the idea of an edge connecting two nodes within the social network
    '''

    # data attributes of a Friend
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Returns a string representation of this Friend relationship
        '''
        return f'{self.profile1.first_name} & {self.profile2.first_name}'