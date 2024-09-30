## restaurant/urls.py
## description: URL patterns for the restaurant app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    ## all the urls to this app
    path(r'', views.main),
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name='order'),
    path(r'confirmation', views.confirmation, name='confirmation'),
]