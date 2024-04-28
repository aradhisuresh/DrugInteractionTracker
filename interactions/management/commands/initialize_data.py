from django.core.management.base import BaseCommand
# from interactions.import_data import import_drug_data, import_interaction_rules
from interactions.import_data import import_drug_data

class Command(BaseCommand):
    help = 'Initialize drug data and interaction rules'

    def handle(self, *args, **options):
        # Specify the path to the CSV file
        csv_file_path = r'C:\Users\Varuni Ramesh\Downloads\Drug-Interaction\Drugs2.csv'

        # Import drug data if not already present
        import_drug_data(csv_file_path)

        # Import interaction rules if not already present
        # import_interaction_rules()

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
