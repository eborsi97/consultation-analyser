import functools

import httpx
import testino

import consultation_analyser.wsgi

TEST_SERVER_URL = "http://consultation-analyser-testserver:8000/"


def with_client(func):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        with httpx.Client(app=consultation_analyser.wsgi.application, base_url=TEST_SERVER_URL) as client:
            return func(client, *args, **kwargs)

    return _inner


def make_testino_client():
    client = testino.WSGIAgent(consultation_analyser.wsgi.application, TEST_SERVER_URL)
    return client
