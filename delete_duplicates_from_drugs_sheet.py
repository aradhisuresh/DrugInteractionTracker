import csv

# Function to clean CSV data
def clean_csv(input_file, output_file, max_length=2000):
    cleaned_data = []
    seen_drugs = set()  # Track seen drug names to remove duplicates

    with open(input_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        for row in reader:
            # Remove duplicates based on drug name
            if row['drug_name'] not in seen_drugs:
                seen_drugs.add(row['drug_name'])

                # Truncate cell values to maximum length
                cleaned_row = {key: value[:max_length] if len(value) > max_length else value for key, value in row.items()}
                cleaned_data.append(cleaned_row)

    # Write cleaned data to a new CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

# Specify input and output file paths
input_csv_file = r'C:\Users\Varuni Ramesh\Downloads\Drug-Interaction\drugs_side_effects_drugs_com.csv'
output_csv_file = r'C:\Users\Varuni Ramesh\Downloads\Drug-Interaction\Drugs.csv'

# Clean the CSV data
clean_csv(input_csv_file, output_csv_file)
