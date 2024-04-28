# from .models import User
# from django.contrib.auth.hashers import make_password
# import jwt
# import datetime
# from django.conf import settings
# from django.utils import timezone

# def register_user(username, email, password):
#     hashed_password = make_password(password)
#     user = User.objects.create(username=username, email=email, password=hashed_password)
#     return user

# def generate_access_token(user):
#     payload = {
#         'user_id': user.id,
#         'exp': timezone.now() + timezone.timedelta(days=1),
#         'iat': timezone.now()
#     }
#     return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

# def generate_refresh_token(user):
#     payload = {
#         'user_id': user.id,
#         'exp': timezone.now() + timezone.timedelta(days=30),
#         'iat': timezone.now()
#     }
#     return jwt.encode(payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')
