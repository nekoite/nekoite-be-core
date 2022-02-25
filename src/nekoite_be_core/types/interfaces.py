import sys
from typing import Any, Union

if sys.version_info < (3, 8):
    from typing_extensions import Protocol, runtime_checkable
else:
    from typing import Protocol, runtime_checkable


__all__ = ["ITransactional", "IStrSerializer"]


@runtime_checkable
class ITransactional(Protocol):
    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


@runtime_checkable
class IStrSerializer(Protocol):
    def dumps(self, obj: Any, *args, **kwargs) -> Union[str, bytes]:
        ...

    def loads(self, s: Union[str, bytes], *args, **kwargs) -> Any:
        ...
