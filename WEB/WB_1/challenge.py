from os import environ
from flask import Flask, Response


app = Flask(__name__)


@app.route("/")
def index():
    return Response(environ["FLAG"], mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
