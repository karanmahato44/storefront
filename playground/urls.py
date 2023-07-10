from django.urls import path
from . import views

urlpatterns = [
    # path() creates/returns a urlpattern object
    path('hello/', views.say_hello, name='storefront-home')
]
