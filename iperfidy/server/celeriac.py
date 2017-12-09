"""Celery Workers"""
# pypi
from celery import Celery


def make_celery(application):
    """makes a celery Task

    Args:
     application: flask app

    Returns:
     Celery: celery decorator with application config added
    """
    celery = Celery(application.import_name,
                    backend=application.config["CELERY_RESULT_BACKEND"],
                    broker=application.config["CELERY_BROKER_URL"])
    celery.conf.update(application.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        """class to adapt Celery to flask"""
        abstract = True

        def __call__(self, *args, **kwargs):
            """adds the application context"""
            with application.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


class CeleryStates:
    """Names for job-states"""
    failure = "FAILURE"
    non_existent = "NON-EXISTENT"
    started = "STARTED"
