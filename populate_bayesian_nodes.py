# populate_bayesian_nodes.py

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Drug_Interaction_Tracker.settings')
django.setup()

from bayesian.models import BayesianNode

def populate_bayesian_nodes():
    # Define the names of Bayesian nodes
    node_names = ['medical_condition', 'side_effects', 'generic_name', 'drug_classes', 'brand_names',
                  'activity', 'rx_otc', 'pregnancy_category', 'csa', 'alcohol', 'related_drugs',
                  'medical_condition_description']
    
    # Create instances of BayesianNode
    for name in node_names:
        node = BayesianNode.objects.create(name=name)
        print(f"Created BayesianNode: {node}")

if __name__ == "__main__":
    # Call the function to populate Bayesian nodes
    populate_bayesian_nodes()
