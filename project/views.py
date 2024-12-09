## project/views.py
## define the views for the project

from django.shortcuts import render

# additional imports
from django.views.generic import ListView, DetailView, TemplateView

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