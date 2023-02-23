import json
import sqlite3
from os import environ, urandom
from uuid import uuid4
from textwrap import dedent
from binascii import hexlify
from http import HTTPStatus
from flask import Flask, request, Response


app = Flask(__name__)

flag = environ["flag"]
flag_piece_len = -(len(flag) // -4)
flag_pieces = [
    flag[i:i+flag_piece_len]
    for i in range(0, len(flag), flag_piece_len)
]

with sqlite3.connect("challenge.db") as db:
    db.execute("CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, csrf TEXT)")


def new_token(session):
    token = hexlify(urandom(8)).decode("ascii")
    with sqlite3.connect("challenge.db") as db:
        db.execute("UPDATE sessions SET csrf=? WHERE id=?", (token, session))
    return token


def error(status, message):
    body = json.dumps({
        "error": status.phrase,
        "message": message
    }, indent=2)
    return Response(body, mimetype="application/json", status=status)


@app.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if username != "admin" or password != "admin":
        return Response(json.dumps({"error": "unauthorized"}, indent=2), mimetype="application/json", status=HTTPStatus.UNAUTHORIZED)
    session = str(uuid4())
    with sqlite3.connect("challenge.db") as db:
        db.execute("INSERT INTO sessions(id) VALUES (?)", (session,))
    response = Response(json.dumps({"status": "ok", "csrf": new_token(session)}, indent=2), mimetype="application/json", status=HTTPStatus.OK)
    response.set_cookie("session", session)
    return response


@app.route("/flag_piece")
def flag():
    session = request.cookies.get("session")
    token = request.args.get("csrf")

    with sqlite3.connect("challenge.db") as db:
        record = db.execute("SELECT csrf FROM sessions WHERE id=?", (session,)).fetchone()

    if record is None:
        return error(HTTPStatus.UNAUTHORIZED, "Bad session")

    expected_token, = record

    if token != expected_token:
        return error(HTTPStatus.UNAUTHORIZED, "Bad csrf token")

    try:
        index = int(request.args["index"])
    except KeyError:
        return error(HTTPStatus.BAD_REQUEST, "Missing index")
    except ValueError:
        return error(HTTPStatus.BAD_REQUEST, "Bad index")

    try:
        if index < 0:
            raise IndexError
        flag_piece = flag_pieces[index]
    except IndexError:
        return error(HTTPStatus.BAD_REQUEST, "Index out of range")

    return Response(
            json.dumps({
                "flag_piece": flag_piece,
                "csrf": new_token(session)
            }, indent=2),
            mimetype="application/json",
            status=HTTPStatus.OK)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
