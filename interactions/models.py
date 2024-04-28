from django.db import models
from django.core.validators import MaxLengthValidator

class Drug(models.Model):
    drug_name = models.CharField(max_length=255,  primary_key=True)
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
    rating = models.FloatField(null=True, blank=True)
    no_of_reviews = models.IntegerField()
    drug_link = models.URLField()
    medical_condition_url = models.URLField()

    def __str__(self):
        return self.drug_name
    
    def save(self, *args, **kwargs):
        # Truncate brand_names if it exceeds the maximum length
        max_length = self._meta.get_field('brand_names').max_length
        self.brand_names = self.brand_names[:max_length]

        if not self.rating:
            self.rating = 0  # Assign a default value of 0 if empty or non-numeric
        elif not isinstance(self.rating, (int, float)):
            try:
                self.rating = float(self.rating)  # Attempt to convert to float
            except (TypeError, ValueError):
                self.rating = 0  # Assign a default value of 0 if conversion fails
        super().save(*args, **kwargs)


class Interaction(models.Model):
    drug_1 = models.ForeignKey(Drug, related_name='interactions_drug_1', on_delete=models.CASCADE)
    drug_2 = models.ForeignKey(Drug, related_name='interactions_drug_2', on_delete=models.CASCADE)
    severity = models.CharField(max_length=20)

    def __str__(self):
        return f"Interaction between {self.drug_1} and {self.drug_2} - Severity: {self.severity}"


class Rule(models.Model):
    rule_id = models.AutoField(primary_key=True, default=None)
    description = models.CharField(max_length=255)
    formula = models.CharField(max_length=255)


    def __str__(self):
        return self.description
