from chalice import Chalice, Response
from chalicelib.schemas import CreateUserSchema, ValidateUserSchema
from marshmallow import ValidationError

app = Chalice(app_name="the-facebook")


@app.route("/v1/ping", methods=["GET"])
def ping():
    return {"success": True}


@app.route("/v1/user", methods=["POST"])
def create_user():
    payload = app.current_request.json_body or {}

    schema = CreateUserSchema()
    try:
        user_id_created = schema.load(payload)
    except ValidationError as err:
        return Response(body=err.messages, status_code=400)

    return Response(body={"user_id": user_id_created}, status_code=201)


@app.route("/v1/user/validate", methods=["POST"])
def validate_user():
    payload = app.current_request.json_body or {}

    schema = ValidateUserSchema()
    try:
        data = schema.load(payload)
    except ValidationError as err:
        return Response(body=err.messages, status_code=400)

    return Response(body=data, status_code=200)
