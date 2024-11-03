# blog/views.py
# define the views for the blog app

from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
import random

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles
    '''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #context variable to use

    def dispatch(self, *args: Any, **kwargs: Any):
        ''' Implement this method to add some debug tracing
        '''
        print(f"ShowAllView.dispatch: self.request.user={self.request.user}")
        return super().dispatch(*args, **kwargs)

class RandomArticleView(DetailView):
    ''' Display one Article selected at Random
    '''
    model = Article # the model to display
    template_name = 'blog/article.html'
    context_object_name = 'article'

    # AttributeError: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # one solution: implement get_object method
    def get_object(self):
        '''Return one Article chosed at random
        '''
        # retrieve all of the objects
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    
class ArticleView(DetailView):
    ''' Display one Article
    '''
    model = Article # the model to display
    template_name = 'blog/article.html'
    context_object_name = 'article'

class CreateCommentView(CreateView):
    ''' A view to create a Comment on an Article
    On GET: send back the form to display
    On POST: read/process the form, and save new Comment to the database
    '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        article = Article.objects.get(pk=self.kwargs['pk'])
        context['article'] = article
        return context

    def get_success_url(self) -> str:
        ''' Return the URL to redirect to on success
        '''
        # return 'show_all'
        # find the Article identified by the PK from the URL pattern
        # article = Article.objects.get(pk=self.kwargs['pk'])
        # return reverse('article', kwargs={'pk':article.pk})
        return reverse('article', kwargs=self.kwargs)
    
    def form_valid(self, form):
        ''' This method is called after the form is validated, before saving data to the database
        '''
        print(f'CreateCommentView.form_valid() form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid() self.kwargs={self.kwargs}')

        # find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])
        # attach this Article to the instance of the Comment to set its FK
        form.instance.article = article
        # delegate work to superclass method
        return super().form_valid(form)
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    ''' A view class to create a new Article instance
    '''
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def form_valid(self, form):
        ''' This method is called as part of the form processing
        '''
        print(f'CreateArticleView.form_valid(): form.cleaned_data={form.cleaned_data}')

        # find the user that's logged in, then attach that user as a FK to the new Article instance
        user = self.request.user
        form.instance.user = user
        # delegate work to superclass method
        return super().form_valid(form)
    
class RegistrationView(CreateView):
    ''' Handle registration of new Users
    '''
    template_name = 'blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        ''' Handle the User creation form submission
        '''
        # if we receive a HTTP POST, we handle it
        if self.request.POST:
            print(f'RegistrationView.dispatch: self.request.POST={self.request.POST}')
            # reconstruct the UserCreationForm from the POST data
            form = UserCreationForm(self.request.POST)
            
            if not form.is_valid():
                print(f'form.errors = {form.errors}')
                return super().dispatch(request, *args, **kwargs)

            # save the form, which creates a new User
            user = form.save()
            print(f'RegistrationView.dispatch: created user {user}')
            # log the User in
            login(self.request, user)
            print(f'RegistrationView.dispatch: {user} logged in')

            # note for mini_fb: attach the FK user to the Profile form instance

            # return a response
            return redirect(reverse('show_all'))
        # let CreateView.dispatch handle the HTTP GET request
        return super().dispatch(request, *args, **kwargs)