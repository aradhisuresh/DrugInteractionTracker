from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Drug, Rule
from django.db import connection
from django.http import JsonResponse


def detect_interaction(drug_a, drug_b):
        # Fetch all rules from the database
        rules = Rule.objects.all()
    
        # Initialize an empty list to store interactions
        interactions = []

        # Iterate over each rule
        for rule in rules:
            # Evaluate the rule's formula using the attributes of the drugs
            try:
                if eval(rule.formula, {'drug_a': drug_a, 'drug_b': drug_b}):
                    interactions.append(rule.description)
            except Exception as e:
                print(f"Error evaluating rule: {e}")

        # Return the list of interactions
        return interactions
    

@api_view(['GET'])
def get_drug_interactions(request):
    drug_a_name = request.query_params.get('drug_a').strip()
    drug_b_name = request.query_params.get('drug_b').strip()

    try:
        print("Drug A Name:", drug_a_name)
        print("Drug B Name:", drug_b_name)
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM Drugs WHERE drug_name = %s", [drug_a_name])
        #     drug_a = cursor.fetchone()
        drug_a = Drug.objects.get(drug_name=drug_a_name)
        drug_b = Drug.objects.get(drug_name=drug_b_name)
        print('Drug-B:', drug_b)
    except Drug.DoesNotExist:
        print(connection.queries[-1]['sql'])

        return Response({"error": "One or both drugs not found"}, status=status.HTTP_404_NOT_FOUND)

    
    
        #  Call the function to check drug interactions
    interactions = detect_interaction(drug_a, drug_b)

    # Return the interactions as JSON response
    return Response({'interactions': interactions})

def get_drug_suggestions(request):
    drug_name_prefix = request.GET.get('name', '')
    drugs = Drug.objects.filter(drug_name__istartswith=drug_name_prefix).values_list('drug_name', flat=True)
    return JsonResponse({'drugs': list(drugs)})