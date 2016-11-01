from django.contrib import admin
from django.db import models

# Register your models here.
from .models import UserRegistration


admin.site.register(UserRegistration)
