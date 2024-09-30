## restaurant/views.py
## description: write view functions to handle URL requests for the restaurant app

from django.shortcuts import render, redirect
import time, random
from datetime import datetime, timedelta

# Create your views here.

def main(request):
    ''' Shows the main page for the restaurant app
    '''
    template_name = 'restaurant/main.html'
    context = {
        'current_time' : time.ctime()
    }
    return render(request, template_name, context)

def order(request):
    ''' Shows the order page, has a daily special item on rotation
    '''
    daily_special = ['Spinach Lasagna With Ricotta', 'Creamy Pumpkin Pasta', 'Spicy Rigatoni With Pork Sugo']
    template_name = 'restaurant/order.html'

    context = {
        'current_time' : time.ctime(),
        'daily_special' : random.choice(daily_special)
    }
    return render(request, template_name, context)

def confirmation(request):
    ''' Shows the confirmation page, determine ordered items and calculate total price
    '''
    if request.POST:
        # Get the form data
        order = request.POST.getlist('pasta')
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        meat = request.POST['meat']

        # random expected time
        random_minutes = random.randint(30, 60)
        expected_time = (datetime.now() + timedelta(minutes=random_minutes)).ctime()

        # count order total
        total = sum([int(item.split('_')[-1]) for item in order])
        food = [item.split('_')[0] for item in order]
        if 'Spaghetti and Meatballs' in food:
            index = food.index('Spaghetti and Meatballs')
            food[index] += ' with ' + meat
            
        template_name = 'restaurant/confirmation.html'
        context = {
            'current_time' : time.ctime(),
            'name' : name,
            'phone' : phone,
            'email' : email,
            'expected_time' : expected_time,
            'total' : total,
            'food' : food,
        }
        return render(request, template_name, context)
    return redirect("order")