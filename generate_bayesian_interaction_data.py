import random
import pyodbc

# Connect to the SQL Server database
conn = pyodbc.connect('Driver={SQL Server};'
    'Server=DESKTOP-A671III\\MSSQLSERVER01;'
    'Database=DrugInteractionTracker;'
    'Trusted_Connection=yes;')

cursor = conn.cursor()

# Create the DrugInteractions table if it doesn't exist
cursor.execute('''IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DrugInteractions_Bayesian')
                  CREATE TABLE DrugInteractions_Bayesian (
                  interaction_id INT IDENTITY(1,1) PRIMARY KEY,
                  drug_a NVARCHAR(255),
                  drug_b NVARCHAR(255),
                  interaction_type NVARCHAR(50),
                  severity NVARCHAR(50)
                  )''')

# Function to generate random drug interactions
def generate_interaction_data(num_interactions):
    interactions = []
    for _ in range(num_interactions):
        # Select two random drugs from the database
        cursor.execute("SELECT TOP 2 drug_name FROM Drugs ORDER BY NEWID()")
        drugs = cursor.fetchall()
        drug_a, drug_b = drugs[0][0], drugs[1][0]
        
        # Randomly generate interaction details
        interaction_details = {
            'drug_a': drug_a,
            'drug_b': drug_b,
            'interaction_type': random.choice(['Moderate', 'Severe', 'None']),
            'severity': random.choice(['Low', 'Medium', 'High'])
        }
        interactions.append(interaction_details)
    
    return interactions

# Generate 1000 random drug interactions
interactions_data = generate_interaction_data(1000)

# Insert the generated interactions into the database table
for interaction in interactions_data:
    cursor.execute("INSERT INTO DrugInteractions_Bayesian (drug_a, drug_b, interaction_type, severity) VALUES (?, ?, ?, ?)",
                   (interaction['drug_a'], interaction['drug_b'], interaction['interaction_type'], interaction['severity']))

# Commit changes and close connection
conn.commit()
conn.close()

print("DrugInteractions_Bayesian data generated and inserted successfully.")
