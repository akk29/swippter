from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from swippter.settings import config
from app.core.logging import Logger

class Command(BaseCommand):

    logger = Logger.get_logger()

    def handle(self, *args, **options):
        self.logger.info('creating admin user')
        User = get_user_model()
        User.objects.create_superuser(
            config("ADMIN_USERNAME"), config("ADMIN_EMAIL"), config("ADMIN_PASSWORD")
        )
        self.logger.info('admin user created')
