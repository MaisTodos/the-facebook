import base64
import uuid

import face_recognition
import pytest
from pytest_chalice.handlers import RequestHandler

from thefacebook.app import app as chalice_app
from thefacebook.chalicelib.models import UserFaces
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


@pytest.fixture(scope="session")
def known_vin_diesel_face():
    image_file = face_recognition.load_image_file("tests/_vin_diesel.jpg")
    return face_recognition.face_encodings(image_file)[0].tolist()


@pytest.fixture(scope="session")
def known_dominic_toretto_face():
    image_file = face_recognition.load_image_file("tests/_dominic_toretto.jpg")
    return face_recognition.face_encodings(image_file)[0].tolist()


@pytest.fixture(scope="session")
def image_without_faces_base64():
    filename = "tests/_image_without_faces.png"
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_base64 = encoded_string.decode()

    return image_base64


@pytest.fixture(scope="session")
def image_with_many_faces_base64():
    filename = "tests/_image_with_many_faces.png"
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_base64 = encoded_string.decode()

    return image_base64


@pytest.fixture(scope="function")
def vin_diesel(known_vin_diesel_face):
    user_id = str(uuid.uuid4())
    UserFaces(id=user_id, faces=[known_vin_diesel_face]).save()

    return UserFaces.get(user_id)
