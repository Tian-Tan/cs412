## project/forms.py
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