# mini_fb/views.py
# define the views for the blog app

from typing import Any
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
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

        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])
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
    
class UpdateProfileView(UpdateView):
    ''' A view to update a profile
    '''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile

    def get_success_url(self):
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_profile', kwargs={'pk':self.object.pk})
    
class DeleteStatusMessageView(DeleteView):
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
    
class UpdateStatusMessageView(UpdateView):
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
    
class CreateFriendView(View):
    ''' A view to create a new Friend relation
    '''
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        other_pk = self.kwargs['other_pk']
        profile = Profile.objects.get(pk=pk)
        other_profile = Profile.objects.get(pk=other_pk)
        profile.add_friend(other_profile)

        return redirect(reverse('show_profile', kwargs={'pk':pk}))
    
class ShowFriendSuggestionsView(DetailView):
    ''' View to show friend suggestions
    '''
    model = Profile # the model to display
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

class ShowNewsFeedView(DetailView):
    ''' View to show all the status messages by the friends of this profile
    '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'