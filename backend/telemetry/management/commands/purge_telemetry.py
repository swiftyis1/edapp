from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from telemetry.models import TelemetryEvent, AuditLog

class Command(BaseCommand):
    help = "Purges student telemetry records older than 1 year (365 days)"

    def handle(self, *args, **options):
        cutoff_date = timezone.now() - timedelta(days=365)
        old_events = TelemetryEvent.objects.filter(timestamp__lt=cutoff_date)
        deleted_count = old_events.count()
        old_events.delete()

        AuditLog.objects.create(
            action_by=None,
            action_name="purge_data",
            description=f"Auto-executed database retention cleaner task: purged {deleted_count} historical telemetry events older than 1 year"
        )
        self.stdout.write(self.style.SUCCESS(f"Successfully purged {deleted_count} historical telemetry events older than 1 year."))
