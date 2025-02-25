from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse 
from paypalrestsdk import Payment
from paypalrestsdk import configure
from django.conf import settings
from .models import Product, Cart, UserProfile 
from django.views import View
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request): 
    return render(request, 'contactus.html')

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        return render(request, "category.html", locals())

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return render(request, 'add_to_cart.html', {'product': product})

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        item.total_price = item.product.discounted_price * item.quantity
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def adjust_cart_item(request, item_id, action):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if action == 'add':
        cart_item.quantity += 1
    elif action == 'remove' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart_view')

@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_amount': total_amount})

def paypal_payment(request):
    configure({
        "mode": "sandbox",
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })

    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
    
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute",
            "cancel_url": "http://localhost:8000/cart/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": item.product.title,
                    "sku": item.product.id,
                    "price": item.product.discounted_price,
                    "currency": "USD",
                    "quantity": item.quantity
                } for item in cart_items]
            },
            "amount": {
                "total": total_amount,
                "currency": "USD"
            },
            "description": "Payment for cart items."
        }]
    })

    if payment.create():
        return redirect(payment.links[1].href)
    else:
        return render(request, 'payment.html', {'error': payment.error})

def payment_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html', {'payment': payment})
    else:
        return render(request, 'payment_failed.html', {'error': payment.error})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['token'] = 'your_generated_token'  
            context = {'username': request.user.username}  
            
            # Check if the user has a profile
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            if created:
                return redirect('profile')  # Redirect to profile creation page
            return redirect('home')  # Redirect to home if profile exists
        else:
            return HttpResponse("Invalid login credentials")
    return render(request, 'login.html')

def registration_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose a different one.")
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return redirect('profile')
    return render(request, 'registration.html')

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created:
        # If a new profile is created, redirect to home
        return redirect('home')
    return render(request, 'profile.html', {'user_profile': user_profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        return redirect('profile')  
    return render(request, 'change_password.html')  

@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_profile.address = request.POST.get('address')
        user_profile.phone = request.POST.get('phone')  
        if 'profile_image' in request.FILES:
            user_profile.profile_image = request.FILES['profile_image']
        user_profile.save()  
        return redirect('profile')
    return render(request, 'update_profile.html', {'user_profile': user_profile})

@login_required
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"
        
        # Send email with the reset link
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return HttpResponse("Password reset link has been sent to your email.")
    return render(request, 'forgot_password.html')

def logout_view(request):
    logout(request)
    return redirect('home')
