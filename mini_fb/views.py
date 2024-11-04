# mini_fb/views.py
# define the views for the blog app

from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add 'is_owner' to context, True if the logged-in user owns the profile
        context['is_owner'] = self.request.user == self.get_object().user
        print(f"ShowProfilePageView: self.request.user = {self.request.user}, self.get_object().user = {self.get_object().user}")
        return context

class CreateProfileView(CreateView):
    ''' A view to create a Profile
    On GET: send back the form to display
    On POST: read/process the form, and save new Profile to the database
    '''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs):
        ''' Add UserCreationForm to the context '''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        # Reconstruct the UserCreationForm with POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Check if both forms are valid
        if user_form.is_valid():
            # Save the User instance
            user = user_form.save()
            print(f'CreateProfileView: created user {user}')
            # log the User in
            login(self.request, user)
            print(f'CreateProfileView: {user} logged in')
            
            # Attach the User to the Profile instance before saving
            form.instance.user = user
            
            # Save the Profile and complete the process by calling superclass form_valid
            return super().form_valid(form)
        else:
            # If the user form is invalid, re-render the form with errors
            return self.form_invalid(form)

    def get_success_url(self):
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_profile', kwargs={'pk':self.object.pk})
    
class CreateStatusView(LoginRequiredMixin, CreateView):
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
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

    def get_success_url(self) -> str:
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_profile', kwargs=self.kwargs)
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
    def form_valid(self, form):
        ''' This method is called after the form is validated, before saving data to the database
        '''
        print(f'CreateStatusView.form_valid() form={form.cleaned_data}')
        print(f'CreateStatusView.form_valid() self.kwargs={self.kwargs}')

        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(user=self.request.user)
        # attach this Profile to the instance of the StatusMessage to set its FK
        form.instance.profile = profile

        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        for file in files:
            # create new image object
            image = Image(
                status = form.instance,
                image_file = file
            )
            image.save()
            print(image)

        # delegate work to superclass method
        return super().form_valid(form)
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' A view to update a profile
    '''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile

    def get_success_url(self):
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_profile', kwargs={'pk':self.object.pk})
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    ''' A view to delete a status message
    '''
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status"

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this status
        pk = self.kwargs.get('pk')
        status = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the profile to which this status is related by FK
        profile = status.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    ''' A view to update a status message
    '''
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage
    context_object_name = "status"

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the update.'''
        # get the pk for this status
        pk = self.kwargs.get('pk')
        status = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the profile to which this status is related by FK
        profile = status.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
class CreateFriendView(LoginRequiredMixin, View):
    ''' A view to create a new Friend relation
    '''
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        other_pk = self.kwargs['other_pk']
        profile = Profile.objects.get(user=user)
        other_profile = Profile.objects.get(pk=other_pk)
        profile.add_friend(other_profile)

        return redirect(reverse('show_profile', kwargs={'pk':profile.pk}))
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' View to show friend suggestions
    '''
    model = Profile # the model to display
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    ''' View to show all the status messages by the friends of this profile
    '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)