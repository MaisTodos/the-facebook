import pytest
from pytest_chalice.handlers import RequestHandler

from thefacebook.app import app as chalice_app


@pytest.fixture()
def api_client():
    return RequestHandler(chalice_app)
