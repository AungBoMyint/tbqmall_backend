from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.core import serializers
from pusher_push_notifications import PushNotifications
import json
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError, DecodeError

beams_client = PushNotifications(
    instance_id='708ffce7-2396-48ec-a338-f9cdf935a978',
    secret_key='C170FEDA038E2AF9F801333CF3932462F420F7D996F3601F719A7C1905F8460C',
)
# Create your views here.
@api_view(['POST'])
def payment_callback(request):
    try:
        response_data = request.data
        response_token = response_data['payload']
        secret_key = 'C170FEDA038E2AF9F801333CF3932462F420F7D996F3601F719A7C1905F8460C'
        try:
            decoded_jwt = jwt.decode(response_token, secret_key, algorithms=["HS256"])
        except (InvalidTokenError, ExpiredSignatureError, DecodeError) as e:
            return Response({'error': 'Invalid or expired token', 'details': str(e)}, status=400)

        # Extract claims
        respCode = decoded_jwt.get("respCode", None)
        if not respCode:
            return Response({'error': 'Payment token not found in the JWT'}, status=400)
        else:
            #request success,return all
            user_id = decoded_jwt.get("userDefined1", None)
            respDesc = decoded_jwt.get("respDesc", None)
            noti_data = {
                "user_ids": [user_id],  # replace with actual user_ids
                "publish_body": {
                    "fcm": {"notification": {"title": respDesc, "body": decoded_jwt}}
                }
            }
            new_request = Request(request=request._request, data=noti_data)
            #push noti to specific device
            push_noti(new_request)

        # Continue processing with payment_token...
        return Response({'response': decoded_jwt})

    except Exception as e:
        return Response({'error': 'An error occurred', 'details': str(e)}, status=500)
        
@api_view(['GET'])
def beams_auth(request,token):
    device_token = token
    beams_token = beams_client.generate_token(device_token)
    return Response(beams_token)
@api_view(['POST'])
def push_noti(request):
    decoded_data = request.data
    beams_client.publish_to_users(
        user_ids=decoded_data["user_ids"],
        publish_body=decoded_data["publish_body"]
    )
    return Response("OK")