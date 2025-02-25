from django.contrib import admin
from .models import Product
from .models import UserProfile  

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address') 
    
class   ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'selling_price', 'discounted_price','description','composition') 
admin.site.register(Product,ProductAdmin)
