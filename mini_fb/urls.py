## mini_fb/urls.py
## description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    ## all the urls to this app
    path(r'', views.ShowAllView.as_view(), name="show_all_profiles"),
]