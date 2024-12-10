## project/forms.py
## Author: Tian Herng Tan (tanth@bu.edu), 12/10/2024
## creates forms for creating new objects

from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    ''' A form to create a new profile
    '''
    class Meta:
        ''' Associate this HTML form with the Profile data model
        '''
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_image']

class UpdateProfileForm(forms.ModelForm):
    ''' A form to update a profile
    '''
    class Meta:
        ''' Associate this HTML form with the Profile data model
        '''
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_image']

class CreateCommentForm(forms.ModelForm):
    ''' A form to add a new comment for a book
    '''
    class Meta:
        ''' Associate this HTML form with the Comment data model
        '''
        model = Comment
        fields = ['comment']

class UpdateCommentForm(forms.ModelForm):
    ''' A form to update a comment
    '''
    class Meta:
        ''' Associate this HTML form with the Comment data model
        '''
        model = Comment
        fields = ['comment']