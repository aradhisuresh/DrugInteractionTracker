from rest_framework.exceptions import AuthenticationFailed
from Drug_Interaction_Tracker.settings import ACCESS_TOKEN_SECRET, REFRESH_TOKEN_SECRET
import jwt
import datetime


def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
        'iat': datetime.datetime.now(datetime.UTC)
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
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=2),
        'iat': datetime.datetime.now(datetime.UTC)
    }, REFRESH_TOKEN_SECRET, algorithm='HS256')


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms='HS256')
        return payload['user_id']
    except:
        raise AuthenticationFailed('Unauthenticated')