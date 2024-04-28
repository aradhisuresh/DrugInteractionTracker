from django.contrib import admin
from django.urls import path, include
from chatbot.views import ChatbotView, UserChatView

urlpatterns = [
path('chatbot/', ChatbotView.as_view(), name='get_chatbot_response'),
path('user/<int:user_id>/chats/', UserChatView.as_view(), name='user-chats'),
]