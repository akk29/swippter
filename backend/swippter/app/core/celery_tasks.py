from django.core.mail import send_mail
from celery import shared_task
from celery.signals import task_prerun, task_postrun, task_failure
from app.core.logging import Logger
from app.utils.utilities import FILLER as F
from swippter.settings import TRIGGER_MAIL_SWITCH

logger = Logger.get_logger()

@task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    logger.info(F.CELERY_TASK_PRERUN.format(task.name,task_id))

@task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    logger.info(F.CELERY_EMAIL_SENT.format(task.name,task_id))

@task_failure.connect
def task_failure_handler(task_id, exception, *args, **kwargs):
    logger.error(F.CELERY_TASK_FAILURE.format(task_id,exception))

@shared_task
def trigger_mail_backround(**kwargs):    
    if TRIGGER_MAIL_SWITCH:
        logger.info(F.CELERY_EMAIL_SENDING)
        subject = kwargs[F.SUBJECT]
        message = kwargs[F.MESSAGE]
        sender = kwargs[F.SENDER]
        reciever = [kwargs[F.RECIEVER]]    
        send_mail(subject,message,sender,reciever)
        logger.info(F.CELERY_EMAIL_SENT)
    else:
        logger.error(F.CELERY_EMAIL_SWITCH_OFF)