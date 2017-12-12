# coding=utf-8
"""Iperf Session feature tests."""

# python standard library
from functools import partial

# from pypi
from expects import (
    be,
    expect,
    raise_error,
    )

from pytest_bdd import (
    given,
    then,
    when,
)
import pytest_bdd

# software under test
from iperfidy.base import IperfSession

# for testing
from ..fixtures import context

and_also = then
scenario = partial(pytest_bdd.scenario,
                   '../../features/base/session.feature')

# ******************** no settings ******************** #


@scenario("A child session doesn't implement the settings definition")
def test_a_child_session_doesnt_implement_the_settings_definition():
    return


@given('a child without a settings definition')
def a_child_without_a_settings_definition(context):
    class NoSettings(IperfSession):
        @property
        def iperf_definition(self):
            return


    context.child = NoSettings
    return


@when('the child is instantiated')
def the_child_is_instantiated(context):
    def bad_call():
        context.child({})
    context.bad_call = bad_call
    return


@then('it raises a TypeError')
def it_raises_a_typeerror(context):
    expect(context.bad_call).to(raise_error(TypeError))
    return

# ******************** no iperf ******************** #


@scenario("A child doesn't implement the iperf definition")
def test_no_iperf_definition():
    return


@given("a child without an iperf definition")
def no_iperf(context):
    class NoIperf(IperfSession):
        @property
        def settings_definition(self):
            return

    context.child = NoIperf
    return

#  When the child is instantiated
#  Then it raises a TypeError

# ******************** Settings ******************** #


@scenario("A child retrieves the settings")
def test_settings():
    return


@given("a child of the iperf session")
def make_session(context, mock):
    context.settings_definition = mock.MagicMock()
    context.settings = mock.MagicMock()
    context.settings_definition.return_value = context.settings

    context.iperf = mock.MagicMock()
    context.iperf_definition = mock.MagicMock()
    context.iperf_definition.return_value = context.iperf
    

    context.json = mock.MagicMock()
    
    class GoodChild(IperfSession):
        @property
        def settings_definition(self):
            return context.settings_definition

        @property
        def iperf_definition(self):
            return context.iperf_definition

    context.child = GoodChild(context.json)
    return


@when("the settings are retrieved")
def get_settings(context):
    context.settings_object = context.child.settings
    expect(context.settings_object).to(be(context.settings))
    return


@then("the expected calls are made")
def check_calls(context):
    context.settings_definition.assert_called_once_with(context.json)
    context.settings.validate.assert_called_once_with()
    return

# ******************** iperf thingy ******************** #


@scenario("A child retrieves the iperf object")
def test_iperf_object():
    return

#  Given a child of the iperf session


@when('the iperf instance is retrieved')
def get_iperf_instance(context):
    context.iperf_object = context.child.iperf
    context.iperf_definition.assert_called_once_with()
    return


@then("it is the expected iperf object")
def check_iperf_instance(context):
    expect(context.iperf_object).to(be(context.iperf))
    return


@and_also("the settings were added to it")
def check_settings_call(context):
    context.settings.assert_called_once_with(context.iperf)
    return

# ******************** call it ******************** #


@scenario("The child is called")
def test_call():
    return

#  Given a child of the iperf session


@when("the child is called")
def call_child(context, mock):
    context.expected_output = {}
    context.result = mock.MagicMock()
    context.result.json = context.expected_output
    context.iperf.run.return_value = context.result
    context.output = context.child()
    return


@then("the iperf is run")
def check_iperf_run(context):
    context.iperf.run.assert_called_once_with()
    return


@and_also("it returns the iperf's json")
def check_returned_value(context):
    expect(context.output).to(be(context.expected_output))
    return

