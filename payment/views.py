from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from pusher_push_notifications import PushNotifications
import json

beams_client = PushNotifications(
    instance_id='708ffce7-2396-48ec-a338-f9cdf935a978',
    secret_key='C170FEDA038E2AF9F801333CF3932462F420F7D996F3601F719A7C1905F8460C',
)
# Create your views here.
@api_view(['POST'])
def payment_callback(request):
    print(request.data)
    return Response(request.data)
@api_view(['GET'])
def beams_auth(request,token):
    device_token = token
    beams_token = beams_client.generate_token(device_token)
    return Response(json.dumps(beams_token))
@api_view(['POST'])
def push_noti(request):
    decoded_data = json.loads(request.data)
    beams_client.publish_to_users(
        user_ids=decoded_data.user_ids,
        publish_body=decoded_data.publish_body
    )
    return Response("OK")