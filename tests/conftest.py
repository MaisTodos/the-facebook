import pytest
from pytest_chalice.handlers import RequestHandler

from thefacebook.app import app as chalice_app
from thefacebook.dynamodb_create_tables import (
    dynamodb_create_tables,
    dynamodb_delete_tables,
)


@pytest.fixture()
def dynamo_setup():
    dynamodb_create_tables()
    yield
    dynamodb_delete_tables()


@pytest.fixture()
def api_client():
    return RequestHandler(chalice_app)
