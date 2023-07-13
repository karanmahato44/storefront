from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('customers/', views.customer_list, name='customers-list'),
    path('customers/<int:id>', views.customer_detail, name='customers-detail'),
    path('products/<int:id>', views.product_detail, name='product-detail'),
    path('collections/', views.collection_list, name='collection-list'),
    path('collections/<int:pk>', views.collection_detail, name='collection-detail'),
]
