import base64
import json
import uuid

import pytest
from chalicelib.models import UserFaces


@pytest.mark.parametrize(
    "image_file_name",
    ("tests/_image_without_faces.png", "tests/_image_many_peoples.png"),
)
def test_validate_user_failure(image_file_name, api_client, dynamo_setup, vin_diesel):
    with open(image_file_name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_base_64 = encoded_string.decode()

    payload = {"user_id": vin_diesel.id, "image_base64": image_base_64}

    response = api_client.post(
        "/v1/user/validate",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )

    assert response.status_code == 400
    assert response.json == {
        "image_base64": ["Deve conter apenas uma pessoa na imagem."]
    }


def test_validate_user_successfully_default_cutoff(
    api_client, dynamo_setup, vin_diesel, known_dominic_toretto_face
):
    vin_diesel.faces.append(known_dominic_toretto_face)
    vin_diesel.save()

    with open("tests/_vin_diesel_small.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_base64 = encoded_string.decode()

    payload = {"user_id": vin_diesel.id, "image_base64": image_base64}

    response = api_client.post(
        "/v1/user/validate",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )

    expected_json = {
        "is_valid": True,
        "cutoff": 0.5,
        "distances": [0.4002920552571979, 0.4018772411248927],
    }
    assert response.status_code == 200
    assert response.json == expected_json

    user_updated = UserFaces.get(str(vin_diesel.id))
    assert len(user_updated.faces) == 3


def test_validate_user_successfully_custom_cutoff(
    api_client, dynamo_setup, vin_diesel, known_dominic_toretto_face
):
    vin_diesel.faces.append(known_dominic_toretto_face)
    vin_diesel.save()

    with open("tests/_vin_diesel_small.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_base64 = encoded_string.decode()

    payload = {"user_id": vin_diesel.id, "image_base64": image_base64, "cutoff": 0.1}

    response = api_client.post(
        "/v1/user/validate",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )

    expected_json = {
        "is_valid": False,
        "cutoff": 0.1,
        "distances": [0.4002920552571979, 0.4018772411248927],
    }
    assert response.status_code == 200
    assert response.json == expected_json

    user_updated = UserFaces.get(str(vin_diesel.id))
    assert len(user_updated.faces) == 2


def test_validate_user_not_found(api_client, dynamo_setup):
    payload = {
        "user_id": str(uuid.uuid4()),
        "image_base64": "some_fake_base64",
    }

    response = api_client.post(
        "/v1/user/validate",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )

    assert response.status_code == 400
    assert response.json == {"user_id": ["Usuário não encontrado."]}


def test_validate_payload_empty(api_client, dynamo_setup):
    payload = {}

    response = api_client.post(
        "/v1/user/validate",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )

    expected_json = {
        "image_base64": ["Missing data for required field."],
        "user_id": ["Missing data for required field."],
    }
    assert response.status_code == 400
    assert response.json == expected_json
