from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('register/', views.register_info, name='register_info'),
    path('create-order/', views.create_order, name='create_order'),
    path('return/', views.payment_return, name='payment_return'),
    path('notify/', views.payment_notify, name='payment_notify'),
    path('query-order/', views.query_order, name='query_order'),
    path('do-register/', views.do_register, name='do_register'),
]
