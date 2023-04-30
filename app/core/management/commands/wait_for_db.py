'''
Django command to wait for the database to br acailable
'''
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for daatabase."""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write('Waiting for database...')
        db_up = False
        count = 0
        while db_up is False or count < 0:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 sec...')
                time.sleep(1)
            count += 1
        if db_up is True:
            self.stdout.write(self.style.SUCCESS('Databsae available'))
        else :
            self.stdout.write(self.style.SUCCESS('Databsae fail'))
