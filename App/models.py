from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY = (
    ('RN', 'RUNNING'),
    ('SN', 'SNEAKER'),
    ('MX', 'MAX'),
    ('DN', 'DUNKS'),
    ('JR', 'JORDAN'),
    ('AR', 'AIR DN'),
    ('FR', 'AIR FORCE'),
    ('VA', 'VAPORFLY'),
    ('VK', 'V2K')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default="")
    prodapp = models.TextField(default="")
    category = models.CharField(choices=CATEGORY, max_length=50)
    product_image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} (by {self.user.username})"

    def get_total_price(self):
        return self.quantity * self.product.discounted_price

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)




    def __str__(self):
        return self.user.username
