import csv
import pyodbc

# Database connection settings
server = r'DESKTOP-A671III\MSSQLSERVER01'
database = 'DrugInteractionTracker'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# CSV file path
csv_file = r'C:\Users\Varuni Ramesh\Downloads\Drug-Interaction\Drugs.csv'

def truncate_brand_names(brand_names):
    # Truncate the brand_names field to 4000 characters
    return brand_names[:4000]


def import_drug_data():
    # Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Open and read the CSV file
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
             #Truncate the brand_names field
            brand_names = truncate_brand_names(row['brand_names'])
            
            # Convert 'no_of_reviews' to integer
            try:
                no_of_reviews = int(row['no_of_reviews'])
            except ValueError:
                # Handle the case where 'no_of_reviews' is not a valid integer
                no_of_reviews = 0  # Or any default value you prefer
            # Insert data into the drugs table
            cursor.execute("""
                INSERT INTO Drugs (drug_name, medical_condition, side_effects, generic_name, drug_classes, brand_names, 
                activity, rx_otc, pregnancy_category, csa, alcohol, related_drugs, medical_condition_description, 
                rating, no_of_reviews, drug_link, medical_condition_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row['drug_name'], row['medical_condition'], row['side_effects'], row['generic_name'], 
                    row['drug_classes'], row['brand_names'], row['activity'], row['rx_otc'], row['pregnancy_category'], 
                    row['csa'], row['alcohol'], row['related_drugs'], row['medical_condition_description'], 
                    row['rating'], no_of_reviews, row['drug_link'], row['medical_condition_url']
                )
            )

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    import_drug_data()
