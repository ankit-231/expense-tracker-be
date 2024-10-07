from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from core.models import Icon


class Command(BaseCommand):
    help = "Populate Icons"

    def handle(self, *args, **options):
        try:
            # populate Icon table
            with transaction.atomic():
                if not Icon.objects.exists():
                    self._populate_icons()
                    self.stdout.write(
                        self.style.SUCCESS("Icon table populated successfully!")
                    )

        except Exception as e:
            raise CommandError(f"Error during initial server setup: {e}")

    def _populate_icons(self):
        """
        populates icons that have not already been added
        """
        try:
            from utilities.svgs import svgs
        except ImportError:
            raise CommandError(
                "Error during initial server setup: svgs module not found"
            )
        existing_icons = Icon.objects.values_list("name", flat=True)
        svgs = [icon for icon in svgs if icon["name"] not in existing_icons]
        Icon.objects.bulk_create(
            [
                Icon(
                    name=icon["name"],
                    svg_data=icon["svg_data"],
                )
                for icon in svgs
            ]
        )
