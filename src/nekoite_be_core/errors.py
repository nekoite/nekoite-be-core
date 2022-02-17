from nekoite_be_core.view import Response


__all__ = ["BEError"]


class BEError(RuntimeError, Response):
    def __init__(self, code: int, message: str = None, data: str = None) -> None:
        Response.__init__(self, code, message, data)
        RuntimeError.__init__(self, message)
