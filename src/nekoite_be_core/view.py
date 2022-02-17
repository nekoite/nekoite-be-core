from typing import Any, Dict, Union, Iterable, Type, Optional
from abc import ABC, abstractmethod
from marshmallow import Schema


__all__ = ["Response", "ViewBase", "FrameworkAdapterBase", "register_routes"]


class Response:
    def __init__(self, code: int, message: Optional[str], data: Any) -> None:
        self._code = code
        self._message = message
        self._data = data

    @property
    def code(self) -> int:
        return self._code

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def data(self) -> Any:
        return self._data


class ViewBase(ABC):
    _is_json_body_ = True

    request_schema: Dict[str, Any]
    response_schema: Dict[str, Any]
    methods: Union[Iterable[str], str]

    def __init__(self):
        self._req_sch: Schema = (
            Schema.from_dict(self.request_schema)()
            if getattr(self, "request_schema", None) is not None
            else None
        )
        self._resp_sch: Schema = (
            Schema.from_dict(self.response_schema)()
            if getattr(self, "response_schema", None) is not None
            else None
        )

    def parse_request(self, req: Dict[str, Any]) -> Dict[str, Any]:
        if not self._req_sch:
            return req
        return self._req_sch.load(req)

    @abstractmethod
    def handle_req(self, req: Dict[str, Any]) -> Any:
        raise NotImplementedError()

    def parse_response(self, resp: Any) -> Any:
        if not isinstance(resp, dict) or not self._resp_sch:
            return resp
        return self._resp_sch.dump(resp)


class FrameworkAdapterBase(ABC):
    @abstractmethod
    def register_route(self, route: str, view: ViewBase):
        raise NotImplementedError()


def register_routes(
    adapter: FrameworkAdapterBase,
    routes: Dict[str, Type[ViewBase]],
    strict_trailing_slash: bool = True,
):
    for route, view in routes.items():
        adapter.register_route(route, view())
        if not strict_trailing_slash:
            another_rt = route
            if route.endswith("/"):
                another_rt = route[:-1]
            else:
                another_rt = route + "/"
            if another_rt not in routes:
                adapter.register_route(another_rt, view())
