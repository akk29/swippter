from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from swippter.settings import config
from app.core.logging import Logger
from app.utils.utilities import F

class Command(BaseCommand):

    logger = Logger.get_logger()

    def handle(self, *args, **options):
        self.logger.info(F.CREATING_ADMIN_USER)
        User = get_user_model()
        try:            
            User.objects.get(email=config(F.ADMIN_EMAIL))
            self.logger.info(F.ADMIN_USER_ALREADY_REGISTERED)
        except User.DoesNotExist:
            User.objects.create_superuser(config(F.ADMIN_EMAIL), config(F.ADMIN_PASSWORD))
            self.logger.info(F.ADMIN_USER_REGISTERED)