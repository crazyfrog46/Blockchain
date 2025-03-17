from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, home_view, purchase_product, purchase_confirmation_view, product_list, base_view

urlpatterns = [
    path('', base_view, name='base'),  # Root URL for base view
    path('register/', register_view, name='register'),  # Registration view
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login view using Django's built-in LoginView
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout view using Django's built-in LogoutView
    path('home/', home_view, name='home'),  # Home view
    path('buy/<int:product_id>/', purchase_product, name='purchase_product'),  # Purchase product view
    path('purchase_confirmation/<int:product_id>/', purchase_confirmation_view, name='purchase_confirmation'),  # Purchase confirmation view
    path('products/', product_list, name='product_list'),  # Product list view
]