import csv
from django.db import IntegrityError
from .models import Drug, Rule
from bayesian.models import Drug_bayesian
import os

def truncate_brand_names(brand_names):
    # Truncate the brand_names field to 4000 characters
    return brand_names[:4000]

def import_drug_data(csv_file_path):
    # Open and read the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Check if drug already exists
            if not Drug.objects.filter(drug_name=row['drug_name']).exists() and \
                    not Drug_bayesian.objects.filter(drug_name=row['drug_name']).exists():
                # Truncate the brand_names field
                brand_names = truncate_brand_names(row['brand_names'])
                
                # Convert 'no_of_reviews' to integer
                try:
                    no_of_reviews = int(row['no_of_reviews'])
                except ValueError:
                    # Handle the case where 'no_of_reviews' is not a valid integer
                    no_of_reviews = 0  # Or any default value you prefer
                    
                # Insert data into the drugs table
                drug = Drug(
                    drug_name=row['drug_name'], medical_condition=row['medical_condition'],
                    side_effects=row['side_effects'], generic_name=row['generic_name'],
                    drug_classes=row['drug_classes'], brand_names=brand_names,
                    activity=row['activity'], rx_otc=row['rx_otc'],
                    pregnancy_category=row['pregnancy_category'], csa=row['csa'],
                    alcohol=row['alcohol'], related_drugs=row['related_drugs'],
                    medical_condition_description=row['medical_condition_description'],
                    rating=row['rating'], no_of_reviews=no_of_reviews,
                    drug_link=row['drug_link'], medical_condition_url=row['medical_condition_url']
                )
                drug.save()

                # Insert data into the Drug_bayesian table
                drug_bayesian = Drug_bayesian(
                    drug_name=row['drug_name'], medical_condition=row['medical_condition'],
                    side_effects=row['side_effects'], generic_name=row['generic_name'],
                    drug_classes=row['drug_classes'], brand_names=brand_names,
                    activity=row['activity'], rx_otc=row['rx_otc'],
                    pregnancy_category=row['pregnancy_category'], csa=row['csa'],
                    alcohol=row['alcohol'], related_drugs=row['related_drugs'],
                    medical_condition_description=row['medical_condition_description']
                )
                drug_bayesian.save()


def import_interaction_rules():
    # Define generic interaction rules
    generic_rules = [
        {
            'description': "If both drugs belong to the same drug class, monitor for potential interactions.",
            'formula': "drug_a.drug_classes == drug_b.drug_classes",
        },
        {
            'description': "If one drug has a higher pregnancy category than the other, monitor for potential interactions.",
            'formula': "drug_a.pregnancy_category > drug_b.pregnancy_category",
        },
        {
            'description': "If either drug interacts with alcohol, monitor for potential interactions.",
            'formula': "drug_a.alcohol == 'Y' or drug_b.alcohol == 'Y'",
        },
        {
            'description': "If both drugs share common side effects, monitor for potential interactions.",
            'formula': "set(drug_a.side_effects.split()) & set(drug_b.side_effects.split())",
        },
        {
            'description': "If one drug inhibits the activity of the other, monitor for potential interactions.",
            'formula': "drug_a.inhibits == drug_b.generic_name",
        },
        # Add more generic rules here...
    ]

    # Insert generic rules into the database table
    for rule_data in generic_rules:
        try:
            Rule.objects.create(**rule_data)
        except IntegrityError:
            # Rule already exists, skip insertion
            pass

if __name__ == "__main__":
    # Specify the path to the CSV file
    # Get the directory of the current script
    csv_file_path = csv_file_path = r'C:\Users\Varuni Ramesh\Downloads\Drug-Interaction\Drugs2.csv'


    # Import drug data if not already present
    import_drug_data(csv_file_path)

    # Import interaction rules if not already present
    import_interaction_rules()

    print("Data imported successfully.")
