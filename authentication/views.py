import jwt
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth import authenticate, get_user_model
from .services import register_user, generate_access_token, generate_refresh_token
from .models import BlacklistedToken
from django.conf import settings
from django.contrib.auth import authenticate


User = get_user_model()

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = request.POST
        try:
            username = data['username']
            email = data['email']
            password = data['password']
            user = register_user(username, email, password)
            return JsonResponse({'message': 'User registered successfully', 'user_id': user.id}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Invalid request data'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = request.POST
        try:
            username = data['username']
            password = data['password']
            user = User.objects.get(username=username)
            if user.check_password(password):
                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                return JsonResponse({'access_token': access_token, 'refresh_token': refresh_token}, status=200)
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
            try:
                jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                BlacklistedToken.objects.create(token=token)
                return JsonResponse({'message': 'Logged out successfully'}, status=200)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def refresh_token(request):
    if request.method == 'POST':
        refresh_token = request.POST.get('refresh_token')
        if not refresh_token:
            return JsonResponse({'error': 'Refresh token missing'}, status=400)
        try:
            payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(pk=user_id)
            access_token = generate_access_token(user)
            return JsonResponse({'access_token': access_token}, status=200)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Refresh token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid refresh token'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)