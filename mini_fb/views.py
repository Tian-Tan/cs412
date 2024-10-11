# mini_fb/views.py
# define the views for the blog app

from typing import Any
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
from django.urls import reverse

# class-based view
class ShowAllView(ListView):
    '''the view to show all Profiles
    '''
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' #context variable to use

class ShowProfilePageView(DetailView):
    ''' View to show a single profile
    '''
    model = Profile # the model to display
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    ''' A view to create a Profile
    On GET: send back the form to display
    On POST: read/process the form, and save new Profile to the database
    '''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self):
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_profile', kwargs={'pk':self.object.pk})
    
class CreateStatusView(CreateView):
    ''' A view to create a StatusMessage
    On GET: send back the form to display
    On POST: read/process the form, and save new StatusMessage to the database
    '''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs: Any):
        ''' Creates a context dictionary and add the Profile object to it
        '''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def get_success_url(self) -> str:
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_profile', kwargs=self.kwargs)
    
    def form_valid(self, form):
        ''' This method is called after the form is validated, before saving data to the database
        '''
        print(f'CreateStatusView.form_valid() form={form.cleaned_data}')
        print(f'CreateStatusView.form_valid() self.kwargs={self.kwargs}')

        # find the Article identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # attach this Article to the instance of the Comment to set its FK
        form.instance.profile = profile
        # delegate work to superclass method
        return super().form_valid(form)