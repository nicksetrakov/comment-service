import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from comments.models import Comment
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        users = []
        for i in range(5):
            username = fake.user_name()
            user = User.objects.create_user(
                username=username, email=fake.email(), password="password"
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f"User {username} created"))

        User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin"
        )
        self.stdout.write(self.style.SUCCESS("Superuser created"))

        for _ in range(30):
            parent_comment = None
            if random.choice([True, False]):
                parent_comment = random.choice(Comment.objects.all())

            Comment.objects.create(
                user=random.choice(User.objects.all()),
                email=fake.email(),
                homepage=fake.url(),
                text=fake.text(),
                parent=parent_comment,
            )
        self.stdout.write(
            self.style.SUCCESS("Database populated with fake data")
        )
