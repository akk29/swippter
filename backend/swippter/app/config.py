from django.apps import AppConfig
from app.core.logging import Logger

def setup_logger():
    Logger.setup()    

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.config'

    def ready(self):
        setup_logger()