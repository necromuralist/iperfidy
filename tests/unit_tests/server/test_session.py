# coding=utf-8
"""A Server Session feature tests."""
# python standard library
from functools import partial

# pypi
from pytest_bdd import (
    given,
    then,
    when,
)
import pytest_bdd

# for testing
from ..fixtures import context

scenario = partial(pytest_bdd.scenario,
                   '../../features/server/session.feature')


@scenario('A server session is called')
def test_a_server_session_is_called():
    return


@given('valid settings and a built Server Session')
def valid_settings_and_a_built_server_session(context, faker):
    context.bind_address = faker.ipv4()
    context.port = faker.pyint()
    context.verbose = faker.pybool()    
    return


@when('the server session is called')
def the_server_session_is_called():
    """the server session is called."""


@then('it adds the settings to the server')
def it_adds_the_settings_to_the_server():
    """it adds the settings to the server."""


@then('it creates a server')
def it_creates_a_server():
    """it creates a server."""


@then('it returns the JSON')
def it_returns_the_json():
    """it returns the JSON."""


@then('it runs it')
def it_runs_it():
    """it runs it."""

