from django.db import models

class Drug_bayesian(models.Model):
    drug_name = models.CharField(max_length=255, primary_key=True)
    medical_condition = models.CharField(max_length=255)
    side_effects = models.TextField()
    generic_name = models.CharField(max_length=255)
    drug_classes = models.CharField(max_length=255)
    brand_names = models.CharField(max_length=4000)
    activity = models.CharField(max_length=255)
    rx_otc = models.CharField(max_length=10)
    pregnancy_category = models.CharField(max_length=1)
    csa = models.CharField(max_length=1)
    alcohol = models.CharField(max_length=1)
    related_drugs = models.TextField()
    medical_condition_description = models.TextField()

    class Meta:
        db_table = 'Drugs_bayesian'

    def __str__(self):
        return self.drug_name

class BayesianNode(models.Model):
    name = models.CharField(max_length=255)

class BayesianEdge(models.Model):
    from_node = models.ForeignKey(BayesianNode, on_delete=models.CASCADE, related_name='from_edges')
    to_node = models.ForeignKey(BayesianNode, on_delete=models.CASCADE, related_name='to_edges')
