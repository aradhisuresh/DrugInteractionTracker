from django.urls import path
from bayesian.views import predict_drug_interactions

urlpatterns = [
    path('predict_drug_interactions/', predict_drug_interactions, name='predict_drug_interactions'),
]