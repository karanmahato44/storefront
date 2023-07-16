from django.urls import path
from . import views, views_generic_mixins

urlpatterns = [
    path('products/', views_generic_mixins.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>', views_generic_mixins.ProductDetail.as_view(), name='product-detail'),
    path('collections/', views_generic_mixins.CollectionList.as_view(), name='collection-list'),
    path('collections/<int:pk>', views_generic_mixins.CollectionDetail.as_view(), name='collection-detail'),
    path('customers/', views.CustomerList.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail')
]
