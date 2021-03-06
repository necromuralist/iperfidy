# coding=utf-8
"""Server State feature tests."""
# python standard library
from functools import partial
from http import HTTPStatus
import json

# from pypi
from expects import (
    be_false,
    equal,
    expect,
    have_key,
)
from mockredis import mock_redis_client
from pytest_bdd import (
    given,
    then,
    when,
)
import pytest_bdd

# for testing
from ..fixtures import context

# software under test
from iperfidy.server.api import application
from iperfidy.server.celeriac import CeleryStates

and_also = then

scenario = partial(pytest_bdd.scenario,
                   '../../features/server/server_state.feature')

def setup_mock_celery(context, mock):
    context.start_server_mock = mock.MagicMock(name="start_server_mock")
    mock.patch("iperfidy.server.api.start_server", context.start_server_mock)
    context.mock_job = mock.MagicMock(name="Mock Job")
    context.start_server_mock.AsyncResult.return_value = context.mock_job

    redis = mock_redis_client()
    mock.patch("iperfidy.server.api.redis", redis)
    return
    
# ******************** not running server ******************** #
@scenario("User checks on the server and the job doesn't exist")
def test_user_checks_on_the_server_while_it_isnt_running():
    return


@given('a flask test-client')
def a_flask_testclient(context):
    context.client = application.app.test_client()
    return


@when("the user checks on the server with a bad UUID")
def the_user_checks_on_the_server_and_it_isnt_running(context, mock, faker):
    context.result = None
    setup_mock_celery(context, mock)
    context.mock_job.ready.return_value = False
    context.mock_job.result = context.result
    context.mock_job.state = CeleryStates.pending
    context.uuid = faker.uuid4()
    context.response = context.client.get("/server/{}".format(context.uuid))
    context.data = json.loads(context.response.data)
    context.state = CeleryStates.non_existent
    return

@then('the response is a not-found')
def the_response_is_okay(context):
    expect(context.response.status_code).to(equal(HTTPStatus.NOT_FOUND))
    return

@and_also("it has the expected uuid")
def check_uuid(context):
    expect(context.data["uuid"]).to(equal(context.uuid))
    return

@and_also("it has the expected ready state")
def check_ready(context):
    expect(context.data["ready"]).to(be_false)
    return


@and_also('it has the expected result')
def it_has_the_expected_message(context):
    expect(context.data["result"]).to(equal(context.result))
    return

# ******************** Failed Job ******************** #


@scenario("User checks on the server and the job failed")
def test_failed_job():
    return

#  Given a flask test-client


@when("the user checks on a failed job")
def check_failed_job(context, mock, faker):
    context.uuid = faker.uuid4()
    context.state = CeleryStates.failure
    context.result = None

    setup_mock_celery(context, mock)
    context.mock_job.ready.return_value = False
    context.mock_job.result = context.result
    context.mock_job.state = context.state

    context.response = context.client.get("/server/{}".format(context.uuid))
    context.data = json.loads(context.response.data)
    return


@then("the response is an error")
def check_error(context):
    expect(context.response.status_code).to(equal(HTTPStatus.BAD_REQUEST))
    return

#  And it has the expected message

@and_also("it has the expected state")
def check_state(context):
    expect(context.data["state"]).to(equal(context.state))
    return

# ******************** Okay Job ******************** #


@scenario("User checks on the server and it didn't fail")
def test_okay_job():
    return

#  Given a flask test-client


@when("the user checks on a running or completed job")
def check_okay_job(context, mock, faker):
    context.uuid = faker.uuid4()
    context.state = CeleryStates.running
    context.result = {"some": "thing"}
    setup_mock_celery(context, mock)

    context.mock_job.state = context.state
    context.mock_job.ready.return_value = False
    context.mock_job.result = context.result

    context.response = context.client.get("/server/{}".format(context.uuid))
    context.data = json.loads(context.response.data)
    return


@then("the response is okay")
def check_okay(context):
    expect(context.response.status_code).to(equal(HTTPStatus.OK))
    return

#  And it has the expected state
