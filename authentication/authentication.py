from rest_framework.exceptions import AuthenticationFailed
from Drug_Interaction_Tracker.settings import ACCESS_TOKEN_SECRET, REFRESH_TOKEN_SECRET
import jwt
import datetime
from django.utils import timezone



def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': timezone.now() + datetime.timedelta(minutes=5),
        'iat': timezone.now()
    }, ACCESS_TOKEN_SECRET, algorithm='HS256')


def decode_access_token(token):
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=['HS256'])
        return payload['user_id']
    except:
        raise AuthenticationFailed('Unauthenticated')


def create_refresh_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': timezone.now() + datetime.timedelta(days=2),
        'iat': timezone.now()
    }, REFRESH_TOKEN_SECRET, algorithm='HS256')


def decode_refresh_token(token):
    try:
        print('Refresh Token from decode_refresh_token method: ', token)
        print('Refresh_Token_Secret from decode_refresh_token method: ', REFRESH_TOKEN_SECRET)

        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms='HS256')
        print('UserId: ', payload['user_id'])
        return payload['user_id']
    except:
        raise AuthenticationFailed('Unauthenticated')