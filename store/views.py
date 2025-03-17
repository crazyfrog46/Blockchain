from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import UserProfile, Product, Purchase
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Custom LoginView using Django's built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Use Django's default authentication template

# Custom LogoutView using Django's built-in LogoutView
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login after logout

# Simplified registration view without complex checks
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if username or password is empty
        if not username or not password:
            return render(request, 'registration/register.html', {'error': 'Username and password are required.'})

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        # Create a user profile upon registration
        UserProfile.objects.get_or_create(user=user)

        # Automatically log the user in after registration
        login(request, user)

        return redirect('home')  # Redirect to home page after successful registration

    return render(request, 'registration/register.html')  # Render the registration page

# Home view for logged-in users
@login_required
def home_view(request):
    return redirect('product_list')  # Redirect to product list view

# Simplified purchase product view with error handling
@login_required
def purchase_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)

        user_wallet = request.user.username  # Assuming wallet is tied to the username

        # Create a purchase record with the user assigned
        purchase = Purchase.objects.create(
            product=product,
            user=request.user,
            user_wallet=user_wallet,
            loyalty_points=10  # 10 points for each purchase
        )

        # Ensure the user has a profile and add loyalty points to it
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.loyalty_points += purchase.loyalty_points
        user_profile.save()

        # Pass the product details to the purchase confirmation view
        return redirect('purchase_confirmation', product_id=product.id)

    return HttpResponse("Unauthorized", status=401)

# Purchase confirmation view
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

# Product list view to display products
def product_list(request):
    products = Product.objects.all()  # Fetch products from the database
    return render(request, 'store/product_list.html', {'products': products})  # Render with products

# View to render the base.html template
def base_view(request):
    return render(request, 'base.html')