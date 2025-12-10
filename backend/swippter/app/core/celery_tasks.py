from django.core.mail import send_mail
from celery.signals import task_prerun, task_postrun, task_failure
from celery import shared_task
from app.core.logging import Logger
from app.utils.utilities import FILLER as F
from swippter.settings import TRIGGER_MAIL_SWITCH

logger = Logger.get_logger()

@task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    logger.info(f"🚀 Task Started: {task.name} [ID: {task_id}]")

@task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    logger.info(f"✅ Task Completed: {task.name} [ID: {task_id}]")

@task_failure.connect
def task_failure_handler(task_id, exception, *args, **kwargs):
    logger.error(f"❌ Task Failed: [ID: {task_id}] - {exception}")

@shared_task
def trigger_mail_backround(**kwargs):    
    if TRIGGER_MAIL_SWITCH:
        logger.info('email sent')
        subject = kwargs[F.SUBJECT]
        message = kwargs[F.MESSAGE]
        sender = kwargs[F.SENDER]
        reciever = [kwargs[F.RECIEVER]]    
        send_mail(subject,message,sender,reciever)
    else:
        logger.error('email switched off')