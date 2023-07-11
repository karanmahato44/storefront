from django.db import models
from django.core.validators import MinValueValidator


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    # sku = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(default='-')
    description = models.TextField(blank=False, null=False)
    unit_price = models.DecimalField(
        max_digits=19, decimal_places=2, blank=False, null=False,
        validators=[MinValueValidator(0)])

    inventory = models.IntegerField(
        blank=False, null=False, validators=[MinValueValidator(0)])

    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # collection = models.ForeignKey('Collection', on_delete=models.CASCADE) - pass a string model if the model to foreign key to is below/parent class can't be on top
    # product_set - default reverse relation but we can use sht like 'products' with related_name
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_BRONZE = 'B'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_BRONZE, 'Bronze')
    ]
    first_name = models.CharField(max_length=225, blank=False, null=False)
    last_name = models.CharField(max_length=225, blank=False, null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=False, null=False)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STAUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STAUS_CHOICES, default=PAYMENT_STATUS_PENDING)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=19, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=False, blank=False)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)
    zip = models.CharField(max_length=10, null=True, blank=True)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
