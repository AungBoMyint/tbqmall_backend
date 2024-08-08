from django.urls import path
from .views import payment_callback,beams_auth,push_noti

urlpatterns = [
    path('callback/',payment_callback,name='payment-callback'),
    path('beams_auth/<str:token>/',beams_auth,name='auth'),
    path('push_noti/',push_noti,name='noti')
]
