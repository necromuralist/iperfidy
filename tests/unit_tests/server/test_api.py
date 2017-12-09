# coding=utf-8
"""Server API feature tests."""
# python standard library
from functools import partial

# from pypi
from pytest_bdd import (
    given,
    then,
    when,
)
import pytest_bdd

# software under test
# from iperfidy.server.api import start_server

# for testing
from ..fixtures import context

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


#@scenario('start_server is called')
#def test_start_server_is_called():
#    return
#
#
#@given('the server API')
#def the_server_api(context):    
#    return
#
#
#@when('start_server is called')
#def start_server_is_called(context, mock):
#    context.self_mock = mock.MagicMock()
#    context.celery = CeleryMock(context.self_mock)
#    mock.patch("iperfidy.server.api.celery", context.celery)
#    context.parameters = mock.MagicMock()
#    start_server(context.parameters)
#    return
#
#
#@then('it updates the state')
#def it_updates_the_state(context):
#    context.self_mock.update_state.assert_called_once_with()
#
#
#@then('returns the output of the server session')
#def returns_the_output_of_the_server_session():
#    """returns the output of the server session."""
#
#
#@then('starts the ServerSession')
#def starts_the_serversession():
#    """starts the ServerSession."""

