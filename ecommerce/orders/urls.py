from django.urls import path
from . import views

urlpatterns = [
  path('place_order/', views.place_order, name='place_order'),
  path('payment/', views.payment, name='payment'),
  path('order_successful/', views.order_successful, name='order_successful'),
]