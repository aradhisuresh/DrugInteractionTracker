from django.urls import path
from .views import get_drug_interactions

urlpatterns = [
    path('api/get_drug_interactions/', get_drug_interactions, name='get_drug_interactions'),
]