## hw/views.py
## description: write view functions to handle URL requests for the hw app
 
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time, random

# Create your views here.
# def home(request):
#     '''Handles the main URL for the hw app'''

#     response_text = f'''
#     <html>
#     <h1>Hello, world!</h1>
#     <p>This is our first django web application!</p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </html>'''

#     # create and return a response to the client:
#     return HttpResponse(response_text)

def home(request):
    '''
    Function to handle the URL request for /hw/home (home page)
    Delegate rendering to the template hw/home.html
    '''
    # use this template to render the response
    template_name = 'hw/home.html'

    # create context variables
    context = {
        'current_time' : time.ctime(),
        'letter1' : chr(random.randint(65,90)),
        'letter2' : chr(random.randint(65,90)),
        'number' : random.randint(1,10),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /hw/about (home page)
    Delegate rendering to the template hw/about.html
    '''
    # use this template to render the response
    template_name = 'hw/about.html'

    # create context variables
    context = {
        'current_time' : time.ctime(),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)