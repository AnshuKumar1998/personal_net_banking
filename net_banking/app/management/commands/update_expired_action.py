from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import ActionCenterModel

class Command(BaseCommand):
    help = 'Update actions with expired dates to Incompleted'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        # Filter actions where expire_date has passed and status is 'new'
        expired_actions = ActionCenterModel.objects.filter(expire_date__lt=now, status='new')
        # Update the status of expired actions
        expired_actions.update(status='Incompleted')
        self.stdout.write(self.style.SUCCESS('Successfully updated expired actions'))
