## project/models.py
## Author: Tian Herng Tan (tanth@bu.edu), 12/10/2024
## define the data objects used in the project

from django.db import models
# authentication imports
from django.contrib.auth.models import User
# additional imports
import uuid, random
from datetime import timedelta
from django.utils.timezone import now

# Create your models here.
class Profile(models.Model):
    ''' Encapsulates the idea of a User Profile
    '''
    # data attributes for a Profile object
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    profile_image = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        ''' Returns a string representation of the Profile Object
        '''
        return f'{self.first_name} {self.last_name}'
    
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
    

class Book(models.Model):
    ''' Encapsulates the idea of a Book in the library management system
    '''
    # data attributes for a Book object
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    description = models.TextField(blank=False)
    genre = models.TextField(blank=False)
    # creates a unique uuid to identify the book, this uuid will also be used in barcode generation
    barcode_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cover_image = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

class Borrow(models.Model):
    ''' Allows many-to-many mapping between Profiles and Books
    '''
    # data attributes for a Borrow object
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=(now() + timedelta(weeks=1))) # set automatically to 1 week from now
    returned_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name} borrowed {self.book.title}'

class Friend(models.Model):
    ''' Encapsulates the idea of a Friend relationship between 2 Profiles
    '''
    # data attributes of a Friend object
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Returns a string representation of this Friend relationship
        '''
        return f'{self.profile1.first_name} & {self.profile2.first_name}'
    
class Comment(models.Model):
    ''' A model for Comments under a Book object
    '''
    # data attributes of a Comment object
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Returns a string representation of this Comment
        '''
        return f'Comment by {self.profile.first_name} {self.profile.last_name} on {self.timestamp} for {self.book}'