from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import TrigramSimilarity

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    brand = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=255, db_index=True)
    nutrition_facts = models.JSONField(blank=True, null=True)
    
    class Meta:
        indexes = [
            GinIndex(fields=['name'], name='product_name_trgm_idx', opclasses=['gin_trgm_ops']),
            GinIndex(fields=['brand'], name='product_brand_trgm_idx', opclasses=['gin_trgm_ops']),
            GinIndex(fields=['category'], name='product_category_trgm_idx', opclasses=['gin_trgm_ops']),
        ]

    def __str__(self):
        return f"{self.name} ({self.brand})"
