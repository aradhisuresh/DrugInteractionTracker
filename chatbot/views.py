from . import askgpt
from .models import Chat
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
from authentication.models import User
import json
from rest_framework.authentication import get_authorization_header
from authentication.authentication import decode_access_token
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed




@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(APIView):
    def post(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1]
            user_id = decode_access_token(token)
            user = User.objects.filter(id=user_id).first()

            if user:
                data = json.loads(request.body)
                message = data.get('message')        
                response = askgpt.ask_openai(message)
                # Save chat to user
                chat = Chat(user=user, message=message, response=response, created_at=timezone.now())
                chat.save()
                return JsonResponse({'message': message, 'response': response})
            else:
                raise AuthenticationFailed('Unauthenticated')
        else:
            raise AuthenticationFailed('Unauthenticated')
