from django.core.management.base import BaseCommand
from products.models import Product
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake products with random nutrition facts'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of products to generate')

    def generate_nutrition_facts(self):
        return {
            'calories': random.randint(50, 500),
            'protein': round(random.uniform(0, 30), 1),
            'carbohydrates': round(random.uniform(0, 50), 1),
            'fat': round(random.uniform(0, 20), 1),
            'fiber': round(random.uniform(0, 10), 1),
            'sugar': round(random.uniform(0, 30), 1),
            'sodium': random.randint(0, 1000),
            'serving_size': f"{random.randint(1, 5)} {random.choice(['oz', 'g', 'ml'])}",
            'servings_per_container': random.randint(1, 10)
        }

    def handle(self, *args, **options):
        count = options['count']
        
        # Sample data for more realistic products
        brands = ['Nestle', 'Kellogg\'s', 'Coca-Cola', 'PepsiCo', 'Unilever', 
                 'Procter & Gamble', 'Mars', 'Mondelez', 'General Mills', 'Kraft Heinz']
        
        categories = ['Beverages', 'Snacks', 'Breakfast Cereals', 'Canned Goods', 
                     'Dairy Products', 'Frozen Foods', 'Bakery', 'Confectionery', 
                     'Health Foods', 'Ready-to-Eat Meals']

        for _ in range(count):
            product = Product.objects.create(
                name=fake.word().capitalize() + ' ' + fake.word().capitalize(),
                brand=random.choice(brands),
                category=random.choice(categories),
                nutrition_facts=self.generate_nutrition_facts()
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} products')
        ) 