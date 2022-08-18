from chalicelib.models import UserFaces


def test_dynamodb_config(dynamo_setup):
    assert UserFaces.Meta.host == "http://dynamodb-test:8000"
