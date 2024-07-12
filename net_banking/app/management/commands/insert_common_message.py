from django.core.management.base import BaseCommand
from app.models import Account_holders, User_Inbox
from django.utils import timezone


class Command(BaseCommand):
    help = 'Insert a common message for every user'

    def handle(self, *args, **kwargs):
        common_subject = 'Welcome Message'
        common_content = 'This is a common message for all users.'

        users = Account_holders.objects.all()
        for user in users:
            User_Inbox.objects.create(
                user=user,
                username=user.username,
                name=user.name,
                email=user.email,
                mobile=user.mobile,
                subject=common_subject,
                content=common_content,
                date=timezone.now().date()
            )

        self.stdout.write(self.style.SUCCESS('Tomorrow will be holiday'))


# python manage.py insert_common_message  (this is command for run this file)
