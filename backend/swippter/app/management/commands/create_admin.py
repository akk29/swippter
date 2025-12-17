from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from swippter.settings import config
from app.core.logging import Logger
from app.utils.utilities import F, is_valid_email

class Command(BaseCommand):

    logger = Logger.get_logger()

    def handle(self, *args, **options):
        self.logger.info(F.CREATING_ADMIN_USER)
        User = get_user_model()
        admin_email, admin_password, validation_failed = (
            config(F.ADMIN_EMAIL),
            config(F.ADMIN_PASSWORD),
            False,
        )
        if admin_email is None or not is_valid_email(admin_email):
            self.logger.error(F.ERROR_IN_ADMIN_EMAIL)
            validation_failed = True
        if admin_password is None or len(admin_password) < 1:
            self.logger.error(F.ERROR_IN_ADMIN_PASSWORD)
            validation_failed = True
        if not validation_failed:
            try:
                User.objects.get(email=admin_email)
                self.logger.error(F.ADMIN_USER_ALREADY_REGISTERED)
            except User.DoesNotExist:
                User.objects.create_superuser(admin_email, admin_password)
                self.logger.info(F.ADMIN_USER_REGISTERED)
        else:
            self.logger.error(F.ADMIN_USER_NOT_REGISTERED)