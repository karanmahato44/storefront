from django.urls import path, include
from . import views, views_generic_mixins, views_viewset
from rest_framework_nested import routers


# router = SimpleRouter()
router = routers.DefaultRouter()
router.register('products', views_viewset.ProductViewSet, basename='products')
router.register('collections', views_viewset.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views_viewset.ReviewViewSet, basename='product-reviews')
# urlpatterns = [
#     path('products/', views_generic_mixins.ProductList.as_view(), name='product-list'),
#     path('products/<int:pk>', views_generic_mixins.ProductDetail.as_view(), name='product-detail'),
#     path('collections/', views_generic_mixins.CollectionList.as_view(), name='collection-list'),
#     path('collections/<int:pk>', views_generic_mixins.CollectionDetail.as_view(), name='collection-detail'),
#     path('customers/', views.CustomerList.as_view(), name='customer-list'),
#     path('customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail')
# ]

# urlpatterns = router.urls + products_router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
