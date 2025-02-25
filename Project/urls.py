from django.contrib import admin
from django.urls import path
from App import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/', views.paypal_payment, name='payment'),  
    path('payment/execute/', views.payment_execute, name='payment_execute'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('adjust-cart-item/<int:item_id>/<str:action>/', views.adjust_cart_item, name='adjust_cart_item'),
    path('login/', views.login_view, name='login'),  
    path('register/', views.registration_view, name='registration'),  
    path('logout/', views.logout_view, name='logout'),  
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),  
    path('forgot-password/', views.forgot_password, name='forgot_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
