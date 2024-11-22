## project/views.py
## define the views for the project

from django.shortcuts import render

# additional imports
from django.views.generic import ListView

# import other components
from .models import *
from .forms import *

# Create your views here.
class ShowAllBooksView(ListView):
    ''' A view to show all Books currently available
    '''
    model = Book
    template_name = 'project/show_all_books.html'
    context_object_name = 'books'

class ShowAllProfilesView(ListView):
    ''' A view to show all Profiles
    '''
    model = Profile
    template_name = 'project/show_all_profiles.html'
    context_object_name = 'profiles'