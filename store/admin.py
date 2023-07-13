from typing import Any, List, Optional, Tuple
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models import Count
from .models import Product, Customer, Collection, Order, OrderItem


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tag']
    prepopulated_fields = {
        'slug': ['title']
    }
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 50
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_records = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_records} product were updated successfully.'
        )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 50
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    min_num = 1
    max_num = 10
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']
    list_select_related = ['customer']
    inlines = [OrderItemInline]

    def customer(self, order):
        return order.customer.first_name


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode(
            {
                'collection_id': str(collection.id)
            }
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
