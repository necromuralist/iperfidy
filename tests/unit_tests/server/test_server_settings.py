"""Server Settings feature tests."""
# python standard library
from functools import partial

# pypi
from expects import (
    expect,
    raise_error,
)
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
from iperfidy.server.server_settings import (
    ServerSettings,
)

scenario = partial(pytest_bdd.scenario,
                   '../../features/server/server_settings.feature')


@scenario('A valid JSON settings is validated')
def test_a_valid_json_settings_is_validated():
    return

    
@given('a Server Settings with valid JSON')
def a_server_settings_with_valid_json(context):
    context.settings = ServerSettings({})
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


@when('the invalid JSON is validate')
def the_invalid_json_is_validate(context):
    def bad_validation():
        context.settings.validate()
    context.validate = bad_validation
    return


@then('it raises an InvalidServerSettings error')
def it_raises_an_invalidserversettings_error(context):
    expect(context.validate).to(raise_error(InvalidSettings))
    return
