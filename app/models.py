from __future__ import unicode_literals
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
import datetime as dt
from django.urls import reverse

# Create your models here.

FLAVOUR_CHOICES = (
    ('CHOCOLATE FUDGE', 'CHOCOLATE FUDGE'),
    ('CHOCOLATE MINT', 'CHOCOLATE MINT'),
    ('CHOCOLATE CHIP', 'CHOCOLATE CHIP'),
    ('RED VELVET', 'RED VELVET'),
    ('BLUE VELVET', 'BLUE VELVET'),
    ('GREEN VELVET', 'GREEN VELVET'),
    ('VANILLA', 'VANILLA'),
    ('COFFEE', 'COFFEE'),
    ('COCONUT', 'COCONUT'),
    ('GINGER', 'GINGER'),
    ('ZEBRA', 'ZEBRA'),
    ('CINNAMON', 'CINNAMON'),
    ('SPICE', 'SPICE'),
    ('MARBLE', 'MARBLE'),
    ('PINA COLADA', 'PINA COLADA'),
    ('LEMON', 'LEMON'),
    ('LIME', 'LIME'),
    ('BANANA', 'BANANA'),
    ('ORANGE', 'ORANGE'),
    ('PASSION JUICE', 'PASSION JUICE'),
    ('BUBBLEGUM', 'BUBBLEGUM'),
    ('CARROT', 'CARROT'),
    ('MINT', 'MINT'),
    ('OREO', 'OREO'),
    ('CARAMEL', 'CARAMEL'),
    ('BLUEBERRY', 'BLUEBERRY'),
    ('STRAWBERRY', 'STRAWBERRY'),
    ('BUTTER', 'BUTTER'),
    ('FRUIT', 'FRUIT'),
    ('BLACK FOREST', 'BLACK FOREST'),
    ('WHITE FOREST', 'WHITE FOREST'),
    ('BLUEBERRY FOREST', 'BLUEBERRY FOREST'),
    ('PASSION FRUIT FOREST', 'PASSION FRUIT FOREST'),
)

TOPPINGS_CHOICES = (
    ('SKITTLES', 'SKITTLES'),
    ('GUMMIES', 'GUMMIES'),
    ('FRUITS', 'FRUITS'),
    ('NUTS', 'NUTS'),
    ('OREOS', 'OREOS'),
    ('CHERRIES', 'CHERRIES'),
    ('CAKE SAIL', 'CAKE SAIL'),
    ('CAKE TOPPERS', 'CAKE TOPPERS'),
    ('ASSORTED CHOCOLATES', 'ASSORTED CHOCOLATES'),
)

SIZE_CHOICES =(
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large'),
)

class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    profile_photo = CloudinaryField('image')
    email = models.EmailField(max_length=256, null=True)
    phone = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str___(self):
        return self.phone

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = CloudinaryField('image')
    description = models.TextField(max_length=500, blank=True)
    price = models.FloatField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    flavour =  models.CharField(max_length=60, choices=FLAVOUR_CHOICES, default="VANILLA")
    topping = models.CharField(max_length=60, choices=TOPPINGS_CHOICES, default="GUMMIES")
    size = models.CharField(max_length=60, choices=SIZE_CHOICES, default="Medium")

    class Meta:
        ordering = ('name',)

    def get_url(self):
        return reverse('product_detail', args=[self.category, self.slug])

    def __str__(self):
        return self.name

class VariationManager(models.Manager):
    def flavours(self):
        return super(VariationManager, self).filter(variation_category="flavour",is_active=True)

    def toppings(self):
        return super(VariationManager, self).filter(variation_category="topping",is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category="size",is_active=True)

variation_category_choice=(
    ('flavour', 'flavour'),
    ('topping', 'topping'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) 
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    county = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

class Pay(models.Model):
    first_name = models.CharField(max_length=144, null=True, blank=True)
    last_name = models.CharField(max_length=144, null=True, blank=True)
    phone = models.CharField(max_length=30)


class MpesaPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.TextField()

    class Meta:
        verbose_name = "Mpesa Payment"
        verbose_name_plural = "Mpesa Payments"

    def __str__(self):
        return self.first_name