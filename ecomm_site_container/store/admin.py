from django.contrib import admin
from django.db import models

from .models import Product

admin.site.register(Product)