import base64
import json

from chalicelib.models import UserFaces


def test_create_user_fail_without_faces(
    api_client, dynamo_setup, image_without_faces_base64
):
    payload = {"images_base64": [image_without_faces_base64]}
    response = api_client.post(
        "/v1/user",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )

    assert response.status_code == 400
    assert response.json == {
        "images_base64": ["Deve conter apenas uma pessoa na imagem."]
    }


def test_create_user_fail_with_many_faces(
    api_client, dynamo_setup, image_with_many_faces_base64
):
    payload = {"images_base64": [image_with_many_faces_base64]}
    response = api_client.post(
        "/v1/user",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )

    assert response.status_code == 400
    assert response.json == {
        "images_base64": ["Deve conter apenas uma pessoa na imagem."]
    }


def test_create_user_successfully(api_client, dynamo_setup):
    images = ["tests/_vin_diesel.jpg", "tests/_dominic_toretto.jpg"]
    images_base64 = []

    for image_file_name in images:
        with open(image_file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            images_base64.append(encoded_string.decode())
    payload = {"images_base64": images_base64}

    response = api_client.post(
        "/v1/user",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )

    assert response.status_code == 201
    assert response.json["user_id"] is not None

    user_created = UserFaces.get(response.json["user_id"])
    assert len(user_created.faces) == 2
