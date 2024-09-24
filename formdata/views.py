from django.shortcuts import render, redirect

# Create your views here.

def show_form(request):
    ''' Shows the contact form
    '''
    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    ''' Handles the form submission.
    Reads the form data from the request, and send it back as a template
    '''
    template_name = 'formdata/confirmation.html'

    # check that we have a post request
    if request.POST:
        # read the form data into python variables
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        # package the form data up as context variables for the template
        context = {
            'name' : name,
            'favorite_color' : favorite_color,
        }

        return render(request, template_name, context)
    
    # handle get request on this url
    return redirect("show_form")