from pgmpy.models import BayesianModel
from pgmpy.estimators import ParameterEstimator
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

def build_bayesian_network():
    # Define the structure of the Bayesian network
    model = BayesianModel([('drug_name', 'medical_condition'),
                           ('drug_name', 'side_effects'),
                           ('drug_name', 'drug_classes'),
                           ('drug_name', 'pregnancy_category'),
                           ('drug_name', 'alcohol')])
    
    # Add CPDs (Conditional Probability Distributions) to the model
    cpd_medical_condition = TabularCPD(variable='medical_condition', variable_card=2,
                                       values=[[0.8, 0.2], [0.3, 0.7]],
                                       evidence=['drug_name'], evidence_card=[2])
    model.add_cpds(cpd_medical_condition)
    
    cpd_side_effects = TabularCPD(variable='side_effects', variable_card=2,
                                  values=[[0.7, 0.3], [0.4, 0.6]],
                                  evidence=['drug_name'], evidence_card=[2])
    model.add_cpds(cpd_side_effects)
    
    cpd_drug_classes = TabularCPD(variable='drug_classes', variable_card=2,
                                   values=[[0.9, 0.1], [0.5, 0.5]],
                                   evidence=['drug_name'], evidence_card=[2])
    model.add_cpds(cpd_drug_classes)
    
    cpd_pregnancy_category = TabularCPD(variable='pregnancy_category', variable_card=2,
                                        values=[[0.95, 0.05], [0.4, 0.6]],
                                        evidence=['drug_name'], evidence_card=[2])
    model.add_cpds(cpd_pregnancy_category)
    
    cpd_alcohol = TabularCPD(variable='alcohol', variable_card=2,
                             values=[[0.8, 0.2], [0.3, 0.7]],
                             evidence=['drug_name'], evidence_card=[2])
    model.add_cpds(cpd_alcohol)

    return model



def predict_interaction(model, evidence):
    # Perform inference to predict drug interaction
    inference = VariableElimination(model)
    interaction_probabilities = inference.query(variables=['interaction'], evidence=evidence)
    return interaction_probabilities

# Example usage:
if __name__ == '__main__':
    # Build the Bayesian network
    network = build_bayesian_network()

    # Define evidence for inference
    evidence = {'drug_name': 'DrugA', 'medical_condition': 'ConditionA'}

    # Predict drug interaction
    interaction_probabilities = predict_interaction(network, evidence)
    print(interaction_probabilities)
