from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add', views.add_to_cart, name='add_to_cart'),
    path('cart/delete', views.delete_cart, name='delete_cart')
]
