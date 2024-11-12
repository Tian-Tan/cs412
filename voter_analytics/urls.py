## voter_analytics/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path(r'', VotersListView.as_view(), name="voters"),
    path(r'voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path(r'graphs', GraphListView.as_view(), name="graphs"),
] 
