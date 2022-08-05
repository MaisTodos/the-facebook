from chalice import Chalice

app = Chalice(app_name="the-facebook")


@app.route("/v1/ping")
def ping():
    return {"ping": "pong"}
