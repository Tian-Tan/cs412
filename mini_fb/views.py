# mini_fb/views.py
# define the views for the blog app

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import *

# class-based view
class ShowAllView(ListView):
    '''the view to show all Profiles
    '''
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' #context variable to use