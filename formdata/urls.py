## formdata/urls.py
## description: URL patterns for the formdata app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    ## all the urls to this app
    path(r'', views.show_form, name="show_form"),
    path(r'submit', views.submit, name='submit'),
]