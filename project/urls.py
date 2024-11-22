## project/urls.py

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    ## all the urls to this app
    path(r'', views.ShowAllBooksView.as_view(), name="show_all_books"),
    path(r'all_profiles', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),

    # authentication URLs
    # path(r'login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    # path(r'logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name="logout"),
    # path(r'register/', views.RegistrationView.as_view(), name='register'),
]