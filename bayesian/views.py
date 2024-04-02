from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Drug_bayesian
# from django.db import connection
from bayesian.models import BayesianNode
from django.db import connection
# from .utils import prepare_drug_data
from interactions.views import detect_interaction

@api_view(['GET'])
def get_bayesian_drug_interactions(request):
    drug_a_name = request.query_params.get('drug_a').strip()
    drug_b_name = request.query_params.get('drug_b').strip()

    try:
        drug_a = Drug_bayesian.objects.get(drug_name__iexact=drug_a_name)
        drug_b = Drug_bayesian.objects.get(drug_name__iexact=drug_b_name)
    except Exception as e:
        return Response({"error": "One or both drugs not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check for interactions using predefined rules
    rule_based_interactions = detect_interaction(drug_a, drug_b)

    # Check for interactions using Bayesian network
    bayesian_interactions = []
    try:
        for node in BayesianNode.objects.all():
            if getattr(drug_a, node.name) == getattr(drug_b, node.name):
                bayesian_interactions.append(f"Potential interaction detected: {node.name}")
    except Exception as e:
        print(f"Error detecting Bayesian interactions: {e}")

    interactions = rule_based_interactions + bayesian_interactions

    # Return the interactions as JSON response
    return Response({'interactions': interactions})
