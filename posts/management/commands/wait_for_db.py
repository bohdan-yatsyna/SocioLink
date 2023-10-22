import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command for waiting till database will be available"""

    def handle(self, *args, **options) -> None:
        self.stdout.write("Waiting for database...")
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections["default"].cursor()
            except OperationalError:
                self.stdout.write(
                    "Database unavailable, waiting for  5 seconds..."
                )
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS("Database available!"))
