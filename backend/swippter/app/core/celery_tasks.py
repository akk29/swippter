from celery.signals import task_prerun, task_postrun, task_failure
from app.core.logging import Logger

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