from django.contrib import admin
from .models import Product, Purchase, UserProfile  # Only include the models that exist in your models.py

# Unregister models if they are already registered
from django.contrib.admin.sites import site

models = [Product, Purchase, UserProfile]  # Add all your models here

for model in models:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass  # If the model is not registered, ignore the error

# Register models
for model in models:
    admin.site.register(model)
