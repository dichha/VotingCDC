from django.contrib import admin
from django.db import models

# Register your models here.
from .models import UserLogin


admin.site.register(UserLogin)
