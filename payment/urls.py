from django.urls import path
from .views import payment_callback,beams_auth,push_noti_to_users,push_noti_to_interests

urlpatterns = [
    path('callback/',payment_callback,name='payment-callback'),
    path('beams_auth/<str:token>/',beams_auth,name='auth'),
    path('push_noti_to_users/',push_noti_to_users,name='noti_users'),
    path('push_noti_to_interests/',push_noti_to_interests,name='noti_interests')
]
