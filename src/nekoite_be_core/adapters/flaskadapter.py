import sys
from typing import Callable, Iterable

from nekoite_be_core.view import FrameworkAdapterBase, ViewBase, Response
from nekoite_be_core.util import unify_to_list
from nekoite_be_core.errors import BEError

from marshmallow import ValidationError

try:
    from flask import Flask, request, Response as FlaskResponse
except ModuleNotFoundError:
    print("Module flask is needed to use flask adapter.", file=sys.stderr)
    exit(1)


__all__ = ["default_routefunc_generator", "FlaskAdapter"]


def default_routefunc_generator(
    app: Flask, route: str, view: ViewBase, methods: Iterable[str]
):
    # TODO: support async.
    @app.route(route, endpoint=route, methods=methods)
    def _f_():
        if request.method != "GET" and view._is_json_body_ and not request.is_json:
            raise RuntimeError("Not json post request")
        if request.method in ("PUT", "POST"):
            req = request.json
        else:
            req = request.args
        try:
            req = view.parse_request(req)
        except ValidationError as e:
            # TODO: add customized error processing
            return {"code": 400, "message": str(e)}
        code = 0
        message = ""
        ret = None
        try:
            # if inspect.iscoroutinefunction(view.handle_req):
            #     ret = await view.handle_req(req)
            # else:
            ret = view.handle_req(req)
        except BEError as e:
            code = e.code
            message = e.message if e.message else ""
        except Exception as e:
            code = 500
            # message = traceback.format_exc(1)
            message = str(e)
            raise e
        if isinstance(ret, Response):
            code = ret.code
            message = ret.message
            data = ret.data
        elif isinstance(ret, dict):
            try:
                data = view.parse_response(ret)
            except ValidationError as e:
                code = 500
        elif isinstance(ret, FlaskResponse):
            return ret
        else:
            data = ret

        return {"code": code, "message": message, "data": data}


class FlaskAdapter(FrameworkAdapterBase):
    def __init__(
        self,
        app: Flask,
        routefunc_generator: Callable[
            [Flask, str, ViewBase, Iterable[str]], None
        ] = default_routefunc_generator,
    ) -> None:
        super().__init__()
        self._app = app
        self._routefunc_generator = routefunc_generator

    def register_route(self, route: str, view: ViewBase):
        methods = unify_to_list(view.methods)
        self._routefunc_generator(self._app, route, view, methods)
