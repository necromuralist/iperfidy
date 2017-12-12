"""Server Settings feature tests."""
# python standard library
from functools import partial

# pypi
from expects import (
    equal,
    expect,
    raise_error,
)
from iperf3 import Server
from pytest_bdd import (
    given,
    then,
    when,
)
import pytest_bdd

# for testing
from ..fixtures import context


# software under test
from iperfidy.base import InvalidSettings
from iperfidy.server.settings import (
    ServerSettings,
    ServerSettingsAttributes,
    ServerSettingsKeys,
)

and_also = then
scenario = partial(pytest_bdd.scenario,
                   '../../features/server/server_settings.feature')


# ******************** valid JSON ******************** #
@scenario('A valid JSON settings is validated')
def test_a_valid_json_settings_is_validated():
    return

    
@given('a Server Settings with valid JSON')
def a_server_settings_with_valid_json(context, faker):
    context.bind_address = faker.ipv4()
    context.port = faker.pyint()
    context.verbose = faker.pybool()
    context.settings = ServerSettings({
        ServerSettingsKeys.bind_address: context.bind_address,
        ServerSettingsKeys.port: context.port,
        ServerSettingsKeys.verbose: context.verbose})
    return


@when('the JSON is validated')
def the_json_is_validated(context):
    def check_valid():
        context.settings.validate()
    context.validate = check_valid
    return

@then('nothing happens')
def nothing_happens(context):
    context.validate()
    return

   
# ******************** invalid JSON ******************** #

@scenario('An invalid JSON settings is validated')
def test_an_invalid_json_settings_is_validated():
    return


@given('a Server Settings with invalid JSON')
def a_server_settings_with_invalid_json(context, faker):
    context.bad_key = faker.word()
    context.settings = ServerSettings({context.bad_key: faker.word()})
    return


@when('the invalid JSON is validated')
def the_invalid_json_is_validated(context):
    def bad_validation():
        context.settings.validate()
    context.validate = bad_validation
    return


@then('it raises an InvalidServerSettings error')
def it_raises_an_invalidserversettings_error(context):
    expect(context.validate).to(raise_error(InvalidSettings))
    return


# ******************** call server settings ******************** #


@scenario("An iperf object is passed to the settings")
def test_server_settings_call():
    return

#  Given a Server Settings with valid JSON


@when("the Settings object is passed an iperf object")
def call_server_settings(context, mock):
    context.server = mock.MagicMock()
    context.validation = mock.MagicMock()
    context.settings.validate = context.validation
    context.settings(context.server)
    return


@then("it validates the settings")
def check_validation(context):
    context.validation.assert_called_once_with()
    return


@and_also("transfers the settings to the iperf object")
def check_settings_on_iperf_object(context):
    expect(context.server.bind_address).to(equal(context.bind_address))
    expect(context.server.port).to(equal(context.port))
    expect(context.server.verbose).to(equal(context.verbose))
    return

# ******************** empty settings ******************** #
@scenario("An iperf object is passed to partial settings")
def test_empty_value():
    return


@given("a Server Settings with an empty bind-address")
def set_missing_bind(context, faker):
    context.port = faker.pyint()
    context.verbose = faker.pybool()
    context.settings = ServerSettings({ServerSettingsKeys.bind_address: "",
                                       ServerSettingsKeys.port: context.port,
                                       ServerSettingsKeys.verbose: context.verbose})
    return

#  When the invalid JSON is validated
#  Then it raises an InvalidServerSettings error
