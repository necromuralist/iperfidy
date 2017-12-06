# pypi
from pytest import fixture


class Context(object):
    """something to stick values into"""


@fixture
def context():
    return Context()
