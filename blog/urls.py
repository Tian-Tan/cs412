## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    ## all the urls to this app
    path(r'', views.RandomArticleView.as_view(), name="random"),
    path(r'show_all', views.ShowAllView.as_view(), name="show_all"),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"),
    # path(r'create_comment', views.CreateCommentView.as_view(), name="create_comment"),
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name="create_comment"),
    path(r'create_article', views.CreateArticleView.as_view(), name="create_article"),

    # authentication URLs
    path(r'login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='show_all'), name="logout"),
    path(r'register/', views.RegistrationView.as_view(), name='register'),
]