from django.urls import path
from .views import get_drug_interactions
from .views import get_drug_suggestions

urlpatterns = [
    path('get_drug_interactions/', get_drug_interactions, name='get_drug_interactions'),
    path('drugs/', get_drug_suggestions, name='get_drug_suggestions'),
]