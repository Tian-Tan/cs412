# mini_fb/forms.py
# creates a form for adding new profiles

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' A form to add a new profile on the mino_fb app
    '''
    class Meta:
        ''' Associate this HTML form with the Profile data model
        '''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']
    
class CreateStatusMessageForm(forms.ModelForm):
    ''' A form to add a new status message for a profile
    '''
    class Meta:
        ''' Associate this HTML form with the StatusMessage data model
        '''
        model = StatusMessage
        fields = ['message']