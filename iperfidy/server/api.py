"""The server API"""
# python standard library
from http import HTTPStatus

# pypi
from redis import Redis
redis = Redis()

def get_server_state(uuid):
    """The Current State of the server

    Args:
     uuid (str): identifier for the server job
    """    
    if not redis.exists("celery-task-meta-{}".format(uuid).encode("utf-8")):
        response = {"message": "Unknown job: {}".format(uuid)}, HTTPStatus.NOT_FOUND
    return response
