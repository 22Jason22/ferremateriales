from django.core.management.base import BaseCommand
from inventory.models import Category

class Command(BaseCommand):
    help = 'Populate categories from model choices'

    def handle(self, *args, **options):
        choices = Category.CATEGORY_CHOICES
        for value, display in choices:
            category, created = Category.objects.get_or_create(name=value)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {display}'))
            else:
                self.stdout.write(f'Category already exists: {display}')
