from django.contrib import admin
from django.conf import settings
from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.description


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    def validate_past_date(value):
        if value > timezone.localdate():
            raise ValidationError("Birth date cannot be in the future.")

    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_BRONZE = 'B'

    MEMBERSHIP_CHOICES = [(MEMBERSHIP_GOLD, 'Gold'), (MEMBERSHIP_SILVER, 'Silver'), (MEMBERSHIP_BRONZE, 'Bronze')]

    phone = models.CharField(max_length=20, validators=[RegexValidator(r'^\+?\d{1,3}[-.\s]?\d{1,14}$', 'Enter a valid phone number.')])
    birth_date = models.DateField(null=True, validators=[validate_past_date])
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STAUS_CHOICES = [(PAYMENT_STATUS_PENDING, 'Pending'), (PAYMENT_STATUS_COMPLETE, 'Complete'), (PAYMENT_STATUS_FAILED, 'Failed')]

    payment_status = models.CharField(max_length=1, choices=PAYMENT_STAUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can canel order')
        ]


class OrderItem(models.Model):
    unit_price = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(1)])
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
