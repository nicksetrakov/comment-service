from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = (
        "Check if the database is empty"
        " and populate it with fake data if it is"
    )

    def handle(self, *args, **kwargs):
        self.stdout.write("Checking if database is empty...")
        try:
            connection = connections["default"]
            cursor = connection.cursor()
            # Get a list of models from the "comments" app
            airport_app_config = apps.get_app_config("comments")
            models = airport_app_config.get_models()
            # Check if there are any rows in any of the tables for the models
            is_empty = all(
                self.is_model_table_empty(cursor, model) for model in models
            )

            if is_empty:
                self.stdout.write("Database is empty, generating fake data...")
                call_command("populate_db")
            else:
                self.stdout.write("Database is not empty, no action taken.")
        except OperationalError:
            self.stdout.write("Database is not available.")

    def is_model_table_empty(self, cursor, model):
        table_name = model._meta.db_table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row = cursor.fetchone()
        return row[0] == 0
