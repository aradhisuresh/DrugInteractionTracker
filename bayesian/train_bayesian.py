from bayesian.models import BayesianNode, BayesianEdge
from interactions.utils import prepare_training_data

def train_bayesian_network():
    # Prepare the training data
    training_data = prepare_training_data()

    # Initialize probabilities for each node
    for node in BayesianNode.objects.all():
        node.reset_probabilities()

    # Update probabilities based on training data
    for data_point in training_data:
        for field_name, field_value in data_point.items():
            node = BayesianNode.objects.get(name=field_name)
            node.update_probability(field_value)

    # Normalize probabilities for each node
    for node in BayesianNode.objects.all():
        node.normalize_probabilities()

    # Update conditional probabilities for edges
    for edge in BayesianEdge.objects.all():
        edge.update_conditional_probabilities()

    print("Bayesian network trained successfully.")

if __name__ == "__main__":
    train_bayesian_network()
