# mini_fb/admin.py
# Register the models with the Django Admin tool

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)