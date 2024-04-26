from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from authentication.serializers import UserSerializer
from authentication.models import User
from authentication.authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(request.data['password']):
            raise AuthenticationFailed('Incorrect password')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()
        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token,
        }
        return response


class UserView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1]
            user_id = decode_access_token(token)
            user = User.objects.filter(id=user_id).first()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed('Unauthenticated')


class Refresh(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        user_id = decode_refresh_token(refresh_token)
        access_token = create_access_token(user_id)
        return Response({
            'token': access_token,
        })


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('refreshToken')
        response.data = {
            'message': 'You have successfully logged out',
        }
        return response

# class UserUpdateView(APIView):
#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)