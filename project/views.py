## project/views.py
## define the views for the project

from django.shortcuts import render, get_object_or_404, redirect

# additional imports
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, View, DeleteView
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

    def get_context_data(self, **kwargs):
        ''' Add 'is_owner' to context, True if the logged-in user owns the profile
        '''
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.get_object().user
        return context

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
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' View to show friend suggestions
    '''
    model = Profile # the model to display
    template_name = 'project/friend_suggestions.html'
    context_object_name = 'profile'

    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        ''' Return the Profile who called the add Friend
        '''
        return get_object_or_404(Profile, user=self.request.user)
    
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
        ''' Return the Profile who called the add Friend
        '''
        return get_object_or_404(Profile, user=self.request.user)
    
class CreateCommentView(LoginRequiredMixin, CreateView):
    ''' A view to create a Comment on a Book
    On GET: send back the form to display
    On POST: read/process the form, and save the new Comment to the database
    '''
    form_class = CreateCommentForm
    template_name = "project/create_comment.html"

    def get_context_data(self, **kwargs):
        ''' Creates a context dictionary and adds the Profile and Book objects to it
        '''
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        book = get_object_or_404(Book, pk=self.kwargs['pk'])  # `pk` from the URL corresponds to the Book
        context['profile'] = profile
        context['book'] = book
        return context

    def get_success_url(self):
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_book', kwargs={'pk': self.kwargs['pk']})
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')

    def form_valid(self, form):
        ''' This method is called after the form is validated, before saving data to the database
        '''
        print(f'CreateCommentView.form_valid() form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid() self.kwargs={self.kwargs}')

        # Get the Profile of the logged-in user
        profile = get_object_or_404(Profile, user=self.request.user)

        # Get the Book object identified by the `pk` in the URL
        book = get_object_or_404(Book, pk=self.kwargs['pk'])

        # Associate the Comment instance with the Profile and Book
        form.instance.profile = profile
        form.instance.book = book

        # Delegate saving the form to the superclass method
        return super().form_valid(form)
    
class DeleteCommentView(LoginRequiredMixin, DeleteView):
    ''' A view to delete a comment
    '''
    model = Comment
    template_name = "project/delete_comment.html"
    context_object_name = "comment"

    def get_success_url(self):
        ''' Return the URL to redirect to after the delete
        '''
        # Get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.filter(pk=pk).first()  # Get one object from QuerySet

        # Find the book to which this comment is related by FK
        book = comment.book

        # Reverse to show the book page
        return reverse('show_book', kwargs={'pk': book.pk})

    def get_login_url(self):
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
class UpdateCommentView(LoginRequiredMixin, UpdateView):
    ''' A view to update a comment
    '''
    form_class = UpdateCommentForm
    template_name = "project/update_comment.html"
    model = Comment
    context_object_name = "comment"

    def get_success_url(self):
        ''' Return the URL to redirect to after the update
        '''
        # Get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.filter(pk=pk).first()  # Get one object from QuerySet

        # Find the book to which this comment is related by FK
        book = comment.book

        # Reverse to show the book page
        return reverse('show_book', kwargs={'pk': book.pk})

    def get_login_url(self):
        ''' Return the URL of the login page
        '''
        return reverse('login')