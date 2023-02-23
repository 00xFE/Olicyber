import json
from os import environ
from uuid import uuid4
from textwrap import dedent
from http import HTTPStatus
from flask import Flask, request, Response


app = Flask(__name__)


@app.post("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "admin" and password == "admin":
        return Response(environ["flag"], mimetype="text/plain", status=HTTPStatus.OK)
    else:
        return Response("Bad username or password", mimetype="text/plain", status=HTTPStatus.UNAUTHORIZED)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
