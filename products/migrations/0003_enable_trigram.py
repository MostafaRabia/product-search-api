from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_search_vector_and_more'),
    ]

    operations = [
        TrigramExtension(),
    ] 