# coding=utf-8
"""A Server Session feature tests."""
# python standard library
from functools import partial

# pypi
import iperf3
from expects import (
    be_a,
    expect,
)
from pytest_bdd import (
    given,
    then,
    when,
)
import pytest_bdd

# software under test
from iperfidy.server.session import ServerSession
from iperfidy.server.settings import ServerSettings

# for testing
from ..fixtures import context

and_also = then
scenario = partial(pytest_bdd.scenario,
                   '../../features/server/session.feature')


@scenario('A server session is created')
def test_a_server_session_is_created():
    return


@given('a server session')
def valid_settings_and_a_built_server_session(context, faker):
    context.bind_address = faker.ipv4()
    context.port = faker.pyint()
    context.verbose = faker.pybool()
    context.session = ServerSession(dict(bind=context.bind_address,
                                        port=context.port,
                                        verbose=context.verbose))
    return


@when('the attributes are retrieved')
def the_server_session_is_called(context):
    context.settings = context.session.settings
    context.iperf = context.session.iperf
    return


@then('the settings are server settings')
def it_adds_the_settings_to_the_server(context):
    expect(context.settings).to(be_a(ServerSettings))
    return


@and_also('the iperf attribute is a server')
def it_creates_a_server(context):
    expect(context.iperf).to(be_a(iperf3.Server))
    return
