# coding=utf-8
"""Server State feature tests."""
# python standard library
from functools import partial
from http import HTTPStatus
import json

# from pypi
from expects import (
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
from iperfidy.server.wsgi import application

and_also = then

scenario = partial(pytest_bdd.scenario,
                   '../../features/server/server_state.feature')


# ******************** not running server ******************** #
@scenario("User checks on the server while it isn't running")
def test_user_checks_on_the_server_while_it_isnt_running():
    return


@given('a flask test-client')
def a_flask_testclient(context):
    context.client = application.app.test_client()
    return


@when("the user checks on the server and it isn't running")
def the_user_checks_on_the_server_and_it_isnt_running(context, mock, faker):
    mock.patch("iperfidy.server.api.Redis", mock_redis_client)
    context.response = context.client.get("/server/{}".format(faker.word()))
    return

@then('the response is a not-found')
def the_response_is_okay(context):
    expect(context.response.status_code).to(equal(HTTPStatus.NOT_FOUND))
    return


@and_also('it has the expected message')
def it_has_the_expected_message(context):
    expect(json.loads(context.response.data)).to(have_key("message"))
    return
