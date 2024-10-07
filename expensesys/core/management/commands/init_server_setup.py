from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from core.models import Currency, ServerSetupLog


class Command(BaseCommand):
    help = "Initial server setup, populating currency and other initial data"

    def handle(self, *args, **options):
        try:
            # checking if the setup was run before
            if ServerSetupLog.objects.filter(setup_name="init_server_setup").exists():
                self.stdout.write(
                    self.style.WARNING("Initial server setup has already been run!")
                )
                return

            # populate currency table
            with transaction.atomic():
                if not Currency.objects.exists():
                    self._populate_currency_table()
                    self.stdout.write(
                        self.style.SUCCESS("Currency table populated successfully!")
                    )

                # setup was completed
                ServerSetupLog.objects.create(setup_name="init_server_setup")
                self.stdout.write(
                    self.style.SUCCESS("Initial server setup completed successfully!")
                )

        except Exception as e:
            raise CommandError(f"Error during initial server setup: {e}")

    def _populate_currency_table(self):
        try:
            from utilities.currencies import currencies
        except ImportError:
            raise CommandError(
                "Error during initial server setup: currencies module not found"
            )
        Currency.objects.bulk_create(
            [
                Currency(
                    name=currency["name"],
                    country=currency["country"],
                    symbol=currency["symbol"],
                    code=currency["code"],
                )
                for currency in currencies
            ]
        )
