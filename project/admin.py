## project/admin.py
## Author: Tian Herng Tan (tanth@bu.edu), 12/10/2024
## register the models with the Django Admin portal

from django.contrib import admin

# import models
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Friend)
admin.site.register(Comment)