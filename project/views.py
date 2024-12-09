## project/views.py
## define the views for the project

from django.shortcuts import render, get_object_or_404

# additional imports
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse

# import other components
from .models import *
from .forms import *

# Create your views here.
class HomepageView(TemplateView):
    ''' A view to show a homepage template
    '''
    template_name = 'project/homepage.html'

    def get_context_data(self, **kwargs):
        ''' Add book count and user count to context data
        '''
        # Get the default context data
        context = super().get_context_data(**kwargs)

        # Add additional data for book count and user count
        context['book_count'] = Book.objects.count()
        context['user_count'] = User.objects.count()

        # Add the user's profile if the user is authenticated
        if self.request.user.is_authenticated:
            try:
                context['profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['profile'] = None
        else:
            context['profile'] = None

        return context

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

class ShowBookView(DetailView):
    ''' A view to show a single Book
    '''
    model = Book
    template_name = 'project/show_book.html'
    context_object_name = 'book'

class ShowProfileView(DetailView):
    ''' A view to show a single Profile
    '''
    model = Profile
    template_name = 'project/show_profile.html'
    context_object_name = 'profile'

class SignUpProfileView(CreateView):
    ''' A view to allow for profile sign up
        GET: send back the form for display
        POST: process the form and save the new Profile to the database
    '''
    form_class = CreateProfileForm
    template_name = 'project/sign_up.html'

    def get_context_data(self, **kwargs):
        ''' Add built-in Django UserCreationForm to the context
        '''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        ''' Django user creation, login user, and create profile
        '''
        # Reconstruct the UserCreationForm with POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Check if both forms are valid
        if user_form.is_valid():
            # Save the User instance
            user = user_form.save()
            print(f'SignUpProfileView: created user {user}')
            # log the User in
            login(self.request, user)
            print(f'SignUpProfileView: {user} logged in')
            
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
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' A view to update a profile
    '''
    form_class = UpdateProfileForm
    template_name = "project/update_profile.html"
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
        ''' Return the Profile who called the update
        '''
        return get_object_or_404(Profile, user=self.request.user)