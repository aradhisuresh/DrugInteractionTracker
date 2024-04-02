from .models import Drug, BayesianNode, BayesianEdge

def prepare_training_data():
    # Fetch all drugs from the database
    drugs = Drug.objects.all()

    # Create nodes for drug attributes
    node_names = ['drug_name', 'medical_condition', 'side_effects', 'generic_name', 'drug_classes', 
                  'brand_names', 'activity', 'rx_otc', 'pregnancy_category', 'csa', 'alcohol', 
                  'related_drugs', 'medical_condition_description']

    for name in node_names:
        BayesianNode.objects.get_or_create(name=name)

    # Create edges between nodes
    for i in range(len(node_names)):
        for j in range(i + 1, len(node_names)):
            BayesianEdge.objects.get_or_create(from_node=BayesianNode.objects.get(name=node_names[i]),
                                                to_node=BayesianNode.objects.get(name=node_names[j]))

    # Create training data
    training_data = []

    for drug in drugs:
        data_point = []

        for name in node_names:
            data_point.append(getattr(drug, name))

        training_data.append(data_point)

    return training_data
