## quotes/views.py
## description: write view functions to handle URL requests for the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random, time

# Create your views here.
quotes = ["Hell is other people!", "Man is condemned to be free; because once thrown into the world, he is responsible for everything he does.", "Existence precedes essence."]
images = ["https://3.bp.blogspot.com/-nWUTuaZF8FM/T5Z6fX6YkKI/AAAAAAAACgU/RT7z3js92CU/s1600/jean-paul-sartre-.jpg", "https://i.citations.com/1800x0/smart/2017/02/27/jean-paul-sartre.jpg", "https://images.squarespace-cdn.com/content/v1/5ccc13ba4d871120f830742b/1658494471556-AHOV36FFQ60SCNF53NR9/Jean-Paul-Sartre-Caf%C3%A9.jpg"]

def quote(request):
    '''
    Function to handle the URL request for /quote/ (home page)
    Delegate rendering to the template quotes/quote.html
    '''
    # use this template to render the response
    template_name = 'quotes/quote.html'

    # create context variables
    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
        'current_time' : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    '''
    Function to handle the URL request for /quote/show_all
    Delegate rendering to the template quotes/show_all.html
    '''
    # use this template to render the response
    template_name = 'quotes/show_all.html'

    # create context variables
    context = {
        'quotes': quotes,
        'images': images,
        'current_time' : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /quotes/about
    Delegate rendering to the template quotes/about.html
    '''
    # use this template to render the response
    template_name = 'quotes/about.html'

    # create context variables
    context = {
        'current_time' : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)