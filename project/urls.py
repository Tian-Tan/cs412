## project/urls.py

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    ## all the urls to this app
    path(r'', views.HomepageView.as_view(), name="home"),
    path(r'all_profiles', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'all_books', views.ShowAllBooksView.as_view(), name="show_all_books"),
    path(r'book/<int:pk>', views.ShowBookView.as_view(), name="show_book"),
    path(r'profile/<int:pk>', views.ShowProfileView.as_view(), name="show_profile"),
    path(r'profile/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path(r'profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name="add_friend"),
    path(r'profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name="show_friend_suggestions"),
    path(r'book/<int:pk>/create_comment/', views.CreateCommentView.as_view(), name='create_comment'),
    path(r'comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path(r'comment/<int:pk>/update/', views.UpdateCommentView.as_view(), name='update_comment'),
    path(r'book/<int:pk>/borrow/', views.BorrowBookView.as_view(), name='borrow_book'),
    path(r'borrow/<int:pk>/return/', views.ReturnBookView.as_view(), name='return_book'),
    path(r'statistics', views.BorrowStatisticsView.as_view(), name="borrow_statistics"),
    path(r'book/<int:pk>/qr/', views.BookQRView.as_view(), name='book_qr_code'),
    path(r"scan_qr_code/", views.ScanQRCodeView.as_view(), name="scan_qr_code"),

    # authentication URLs
    path(r'login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name="logout"),
    path(r'sign_up/', views.SignUpProfileView.as_view(), name='sign_up'),
]