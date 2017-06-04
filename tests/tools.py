from nose.tools import *
import re


def assert_response(resp, contains=None, matches=None, headers=None, status="200"):
    assert status in resp.status, "Expected response %r not in %r" % (status,resp.status)

    if status=="200":
        assert resp.data, "Response data is empty."

    if contains:
        assert contains in resp.data, "Response does not contain %r" % contains

    if matches:
        reg = re.compile(matches) # match regex
        assert reg.matches(resp.data), "Response does not match %r" % matches

    if headers:
        assert_equal(resp.headers,headers)


def debug(flag):
    """
    decorator for ignoring test
    :param boolean flag: True means it will be tested
    :return: a decorator
    """
    def testDecorator(aFunc):
        aFunc.__test__ = flag
        return aFunc
    return testDecorator