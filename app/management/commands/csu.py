from django.core.management.base import BaseCommand
from app.models import User

class Command(BaseCommand):
    help = 'Create a default superuser with the email abdullahi@admin.com'

    def handle(self, *args, **kwargs):
        email = 'abdullahi@admin.com'
        password = 'strongPassword123'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING('A user with this email already exists.'))
        else:
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser with email {email}'))
