# coding=utf-8
"""Server API feature tests."""
# python standard library
from functools import partial
from http import HTTPStatus

# from pypi
from expects import (
    be_true,
    equal,
    expect,
)
import mockredis
from pytest_bdd import (
    given,
    then,
    when,
)
import pytest_bdd

# software under test
from iperfidy.server.api import queue_server

# for testing
from ..fixtures import context

and_also = then
scenario = partial(pytest_bdd.scenario,
                   '../../features/server/api.feature')


class CeleryMock(object):
    def __init__(self, self_mock):
        self.self_mock = self_mock
        return

    def task(self, f, bind):        
        def call_it(parameters):
            return f(self.self_mock, parameters)
        return call_it


# ******************** queue server ******************** #

@scenario("The queue_server is called")
def test_queue_server():
    return

@given("the server API")
def server_api_exists():
    return


@when("the queue_server is called")
def call_queue_server(context, mock, faker):
    context.id = faker.uuid4()
    context.server_settings = {faker.word(): faker.word()}
    context.start_server = mock.MagicMock()
    context.delay = mock.MagicMock()
    context.mock_job = mock.MagicMock()
    context.mock_job.id = context.id
    context.delay.return_value = context.mock_job

    context.start_server.delay = context.delay
    mock.patch("iperfidy.server.api.start_server", context.start_server)

    context.redis = mockredis.mock_redis_client()
    mock.patch("iperfidy.server.api.redis", context.redis)
    context.response, context.status_code = queue_server(context.server_settings)
    return


@then("it starts the server")
def check_server_start(context):
    context.delay.assert_called_once_with(parameters=context.server_settings)
    return


@and_also("stores the id in redis")
def check_id_in_redis(context):
    expect(context.id.encode("utf-8") in context.redis.keys()).to(be_true)
    return


@and_also("returns the expected response")
def check_response(context):
    expect(context.status_code).to(equal(HTTPStatus.ACCEPTED))
    return
