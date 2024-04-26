from django.urls import path
from authentication.views import RegisterView, LoginView, UserView, LogoutView, Refresh

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh/', Refresh.as_view()),
    # path('update/<int:pk>', UserUpdateView.as_view()),
]