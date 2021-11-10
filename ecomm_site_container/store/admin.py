from django.contrib import admin
from django.db import models

from .models import Category, EcomUser, Product

admin.site.register(Product)
admin.site.register(EcomUser)
admin.site.register(Category)