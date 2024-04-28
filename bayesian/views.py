from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Drug_bayesian
from bayesian.models import BayesianNode
from interactions.views import detect_interaction
from pgmpy.estimators import BayesianEstimator
from pgmpy.models import BayesianNetwork  
import pandas as pd

@api_view(['GET'])
def predict_drug_interactions(request):
    if request.method == 'GET':
        drug_a_name = request.query_params.get('drug_a')
        drug_b_name = request.query_params.get('drug_b')

        # Retrieve drug instances from the database
        try:
            drug_a = Drug_bayesian.objects.get(drug_name=drug_a_name)
            drug_b = Drug_bayesian.objects.get(drug_name=drug_b_name)
        except Drug_bayesian.DoesNotExist:
            return Response({"error": "One or both drugs not found"}, status=status.HTTP_404_NOT_FOUND)

        # Define the structure of the Bayesian network
        structure = [
            ('medical_condition', 'side_effects'),
            ('drug_classes', 'activity'),
            ('drug_classes', 'pregnancy_category'),
            ('drug_classes', 'csa'),
            ('drug_classes', 'alcohol')
        ]

        # Instantiate the BayesianModel
        model = BayesianNetwork(structure)

        # Get the data from the database
        data = pd.DataFrame([
            [drug_a.medical_condition, drug_a.side_effects,
             drug_a.drug_classes, drug_a.activity,
             drug_a.pregnancy_category, drug_a.csa,
             drug_a.alcohol],
            [drug_b.medical_condition, drug_b.side_effects,
             drug_b.drug_classes, drug_b.activity,
             drug_b.pregnancy_category, drug_b.csa,
             drug_b.alcohol]
        ], columns=['medical_condition', 'side_effects', 'drug_classes', 'activity',
                    'pregnancy_category', 'csa', 'alcohol'])

        # Learn the parameters using Bayesian parameter estimation
        estimator = BayesianEstimator(model, data)

        # Estimate the conditional probability distributions (CPDs)
        cpds = estimator.get_parameters()

        # Initialize response data
        response_data = {
            'overall_interaction_severity': 'Low',  # Default value, will be updated if any attribute has High severity
            'overall_interaction_severity_percentage': 10,
            'interactions': []
        }

        # Combine the probabilities of both drugs for each attribute
        combined_probabilities = {}
        for cpd in cpds:
            variable = cpd.variable
            probabilities = cpd.values
            if variable in combined_probabilities:
                combined_probabilities[variable] *= probabilities
            else:
                combined_probabilities[variable] = probabilities

        # Calculate combined severity for each attribute
        for variable, probabilities in combined_probabilities.items():
            severity_percentage = int(max(probabilities) * 100)  # Convert highest probability to percentage
            severity = 'High' if severity_percentage > 50 else 'Low'

            # Update overall_interaction_severity if any attribute has High severity
            if severity == 'High':
                response_data['overall_interaction_severity'] = 'High'

            affected_attributes = [{'attribute': variable, 'severity': severity}]

            response_data['interactions'].append({
                'variable': variable,
                'severity_percentage': severity_percentage,
                'severity': severity,
                'affected_attributes': affected_attributes
            })

            # Update overall_interaction_severity_percentage
            response_data['overall_interaction_severity_percentage'] += severity_percentage

        # Calculate overall_interaction_severity_percentage
        num_attributes = len(combined_probabilities)
        if num_attributes > 0:
            response_data['overall_interaction_severity_percentage'] //= num_attributes

        # Check if there will be any possible interaction if the two drugs are taken together
        possible_interaction = response_data['overall_interaction_severity'] == 'High'

        response_data['possible_interaction'] = possible_interaction

        return Response(response_data)
