from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, home_view, purchase_product, purchase_confirmation_view, product_list, base_view

urlpatterns = [
    path('', base_view, name='base'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', home_view, name='home'),
    path('buy/<int:product_id>/', purchase_product, name='purchase_product'), 
    path('purchase_confirmation/<int:product_id>/', purchase_confirmation_view, name='purchase_confirmation'),
    path('products/', product_list, name='product_list'),
]