from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import UserProfile, Product, Purchase
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login') 


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        if not username or not password:
            return render(request, 'registration/register.html', {'error': 'Username and password are required.'})

        
        user = User.objects.create_user(username=username, password=password)

        UserProfile.objects.get_or_create(user=user)

        login(request, user)

        return redirect('home')

    return render(request, 'registration/register.html')


@login_required
def home_view(request):
    return redirect('product_list')


@login_required
def purchase_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)

        user_wallet = request.user.username

        purchase = Purchase.objects.create(
            product=product,
            user=request.user,
            user_wallet=user_wallet,
            loyalty_points=10
        )

        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.loyalty_points += purchase.loyalty_points
        user_profile.save()

        return redirect('purchase_confirmation', product_id=product.id)

    return HttpResponse("Unauthorized", status=401)

@login_required
def purchase_confirmation_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        purchase = Purchase.objects.filter(product=product, user=request.user).latest('purchase_date')
    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    except Purchase.DoesNotExist:
        return HttpResponse("Purchase not found", status=404)

    return render(request, 'purchase_confirmation.html', {'product': product, 'loyalty_points': purchase.loyalty_points})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def base_view(request):
    return render(request, 'base.html')