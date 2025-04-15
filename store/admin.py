from django.contrib import admin
from .models import Product, Purchase, UserProfile 


from django.contrib.admin.sites import site

models = [Product, Purchase, UserProfile]

for model in models:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

for model in models:
    admin.site.register(model)
