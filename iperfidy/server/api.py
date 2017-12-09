"""The server API"""
# python standard library
from http import HTTPStatus

# pypi
from flask import url_for
from redis import Redis
import connexion

# this project
from .celeriac import (
    make_celery,
    CeleryStates,
    )

from iperfidy.server.session import ServerSession

redis = Redis()

REDIS_URL = "redis://localhost:6379"


class ServerKeys:
    """holder of string constants"""
    message = "message"
    state = "state"
    ready = "ready"

application = connexion.FlaskApp(__name__)
app = application.create_app()

app.config.update(
    CELERY_BROKER_URL=REDIS_URL,
    CELERY_RESULT_BACKEND=REDIS_URL,
)


celery = make_celery(app)

# ******************** Celery Jobs ******************** #

@celery.task(bind=True)
def start_server(self, parameters): # pragma: no cover
    """adds the server start to celery's queue

    Args:
     parameters(dict): The POST JSON parameters
    """
    self.update_state(state=CeleryStates.started)
    session = ServerSession(parameters)
    return session()
# ******************** The API Functions ******************** #


def queue_server(server_settings):
    """Queues up the iperf server as a celery job

    Args
     server_settings (dict): any server settings
    """
    job = start_server.delay(parameters=server_settings)
    return {"location": "/server/{}".format(job.id)}, HTTPStatus.ACCEPTED


def get_server_state(uuid):
    """The Current State of the server

    Args:
     uuid (str): identifier for the server job
    """
    if not redis.exists("celery-task-meta-{}".format(uuid).encode("utf-8")):
        response = {ServerKeys.message: "Unknown job: {}".format(uuid),
                    ServerKeys.state: CeleryStates.non_existent}, HTTPStatus.NOT_FOUND
    else:
        thing = start_server.AsyncResult(uuid)
        if thing.state != CeleryStates.failure:
            response = ({ServerKeys.message: "Job Found: {}".format(uuid),
                         ServerKeys.state: thing.state,
                         ServerKeys.ready: thing.ready()})
        else:
            response = ({ServerKeys.message: "Job failed: {}".format(uuid),
                        ServerKeys.state: thing.state}, HTTPStatus.BAD_REQUEST)
    return response

# this has to come after the functions because they are referenced in
# the swagger file
application.add_api("swagger.yaml")
