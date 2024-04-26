from django.contrib import admin
from django.urls import path, include
from interactions.views import get_drug_interactions
from bayesian.views import get_bayesian_drug_interactions
from chatbot.views import ChatbotView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/get_drug_interactions/', get_drug_interactions, name='get_drug_interactions'),
    path('api/', include('interactions.urls')),
    path('api/chatbot/', ChatbotView.as_view(), name='get_chatbot_response'),

    
]
