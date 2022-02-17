# run this file with FLASK_APP=examples.example_flask_app flask run

from time import time
import typing as t
from flask import Flask, Response as FlaskResponse
import sys

sys.path.append("src")

from nekoite_be_core.adapters import FlaskAdapter
from nekoite_be_core import ViewBase, register_routes, fields


class TestView(ViewBase):
    request_schema = {"id": fields.Integer(required=True)}
    response_schema = {"id": fields.Integer(), "timestamp": fields.Integer()}
    methods = ["GET", "POST"]

    def handle_req(self, req: t.Dict[str, t.Any]) -> t.Any:
        return {
            "id": req["id"],
            "timestamp": int(time()),
        }
        # return FlaskResponse("abc")  # no schema checking, response can be non-json
        # return "hello, world"        # no schema checking,
        #                                response will be json (data in .data)
        # return 123                   # no schema checking,
        #                                response will be json (data in .data)


app = Flask(__name__)

routes = {"/test": TestView}
adapter = FlaskAdapter(app)

register_routes(adapter, routes)
