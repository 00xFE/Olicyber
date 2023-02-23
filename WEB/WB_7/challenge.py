import json
from os import environ
from uuid import uuid4
from textwrap import dedent
from http import HTTPStatus
from flask import Flask, request, Response


app = Flask(__name__)


@app.route("/")
def root():
    response = Response("Unauthorized", mimetype="text/plain", status=HTTPStatus.UNAUTHORIZED)
    if request.headers.get("X-Method") == "HEAD":
        response.headers["X-Flag"] = environ["flag"]
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
