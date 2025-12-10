from app.core.celery_tasks import trigger_mail_backround

def trigger_user_verification_email(sender,instance,created,**kwargs):
    mail_body = {}       
    trigger_mail_backround.delay(**mail_body)