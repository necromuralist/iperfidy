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
    uuid = "uuid"
    result = "result"

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
    redis.set(job.id, 1)
    return {"location": "/server/{}".format(job.id)}, HTTPStatus.ACCEPTED


def get_server_state(uuid):
    """The Current State of the server

    Args:
     uuid (str): identifier for the server job
    """
    job = start_server.AsyncResult(uuid)
    state = job.state
    status = HTTPStatus.OK

    if state == CeleryStates.pending and not redis.exists(uuid.encode("utf-8")):
        state = CeleryStates.non_existent
        status = HTTPStatus.NOT_FOUND
    elif state == CeleryStates.failure:
        status = HTTPStatus.BAD_REQUEST
        
    response = {ServerKeys.uuid: uuid,
                ServerKeys.state: state,
                ServerKeys.ready: job.ready(),
                ServerKeys.result: job.result}
    return response, status

# this has to come after the functions because they are referenced in
# the swagger file
application.add_api("swagger.yaml")
