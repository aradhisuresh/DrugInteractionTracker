from django.urls import path
from .views import signup, login, logout, refresh_token

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('refresh-token/', refresh_token, name='refresh_token'),

]
