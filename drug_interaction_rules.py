import pyodbc

# Connect to the SQL Server database
conn = pyodbc.connect('Driver={SQL Server};'
    'Server=DESKTOP-A671III\\MSSQLSERVER01;'
    'Database=DrugInteractionTracker;'
    'Trusted_Connection=yes;')

cursor = conn.cursor()

# Create a table to store the rules if it doesn't exist
cursor.execute('''IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'drug_interaction_rules')
    CREATE TABLE drug_interaction_rules (
    rule_id INT PRIMARY KEY,
    description NVARCHAR(255),
    formula NVARCHAR(MAX)
    )''')

# Define more additional rules
more_additional_rules = [
    {
        'rule_id': 1,
        'description': "If Drug A and Drug B belong to the same drug class, monitor for potential interactions.",
        'formula': "drug_a.drug_classes == drug_b.drug_classes and 'Monitor for potential interactions' or 'No interaction'",
    },
    {
        'rule_id': 2,
        'description': "If Drug A has a higher pregnancy category than Drug B, monitor for potential interactions.",
        'formula': "drug_a.pregnancy_category > drug_b.pregnancy_category and 'Monitor for potential interactions' or 'No interaction'",
    },
    {
        'rule_id': 3,
        'description': "If either Drug A or Drug B interacts with alcohol, monitor for potential interactions.",
        'formula': "drug_a.alcohol == 'Y' or drug_b.alcohol == 'Y' and 'Monitor for potential interactions' or 'No interaction'",
    },
    {
        'rule_id': 4,
        'description': "If Drug A and Drug B share common side effects, monitor for potential interactions.",
        'formula': "set(drug_a.side_effects.split()) & set(drug_b.side_effects.split()) and 'Monitor for potential interactions' or 'No interaction'",
    },
    {
        'rule_id': 5,
        'description': "If Drug A inhibits the activity of Drug B, monitor for potential interactions.",
        'formula': "drug_a.inhibits == drug_b.generic_name and 'Monitor for potential interactions' or 'No interaction'",
    },
    # Add more rules here...
]

# Insert the more additional rules into the database table
for rule in more_additional_rules:
    cursor.execute("INSERT INTO drug_interaction_rules (rule_id, description, formula) VALUES (?, ?, ?)",
        (rule['rule_id'], rule.get('description', ''), rule.get('formula', '')))

# Commit changes and close connection
conn.commit()
conn.close()

print("More additional rules inserted successfully into the database.")
