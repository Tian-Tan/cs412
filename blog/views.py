# blog/views.py
# define the views for the blog app

from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
import random

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
from django.urls import reverse

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles
    '''
    model = Article # the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #context variable to use

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