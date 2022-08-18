# criar teste de sucesso com 2 imagens, com mais de 1 rosto e sem nenhum rosto
import base64
import json

import pytest
from chalicelib.models import UserFaces


@pytest.mark.parametrize(
    "image_file_name", ("test/_image_without_faces.png", "test/_image_many_peoples.png")
)
def test_create_user_failure(api_client, dynamo_setup, image_file_name):
    with open(image_file_name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_base_64 = encoded_string

    payload = {"image_base64": [image_base_64]}
    response = api_client.post("/v1/user", body=json.dump(payload))

    assert response.status_code == 400
    assert response.json == {
        "image_base64": ["Deve conter apenas uma pessoa na imagem."]
    }


def test_create_user_successfully(api_client, dynamo_setup):
    images = ["tests/_vin_diesel.jpg", "tests/_dominic_toretto.jpg"]
    images_base_64 = []
    for image_file_name in images:
        with open(image_file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            images_base_64.append(encoded_string)

    payload = {"image_base64": [images_base_64]}
    response = api_client.post("/v1/user", body=json.dump(payload))

    assert response.status_code == 200
    assert response.json["user_id"] is not None

    user_created = UserFaces.get(response.json["user_id"])
    assert len(user_created.faces) == 1
