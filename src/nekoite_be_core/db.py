from typing import Any, Callable, Type, Union

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query, scoped_session, sessionmaker

from nekoite_be_core.types.interfaces import ICommitable as _Commitable

__all__ = ["make_commit_decorator", "ModelBase", "make_model_base"]


def make_commit_decorator(session: _Commitable):
    """
    Generates a decorator that does session.commit() after the function
    is finished.

    Usage:

    ```python
    dbcommit = make_commit_decorator(session)

    @dbcommit
    def add_student():
        s = Student(name="John")
        s.insert()
    ```
    """

    def dbcommit(func: Callable) -> Callable:
        def do_and_commit(*args, **kwargs):
            func(*args, **kwargs)
            session.commit()

        return do_and_commit

    return dbcommit


class ModelBase(declarative_base()):  # type: ignore
    __abstract__ = True

    session: scoped_session
    query: Query

    def save(self):
        self.session.commit()

    def insert(self):
        self.session.add(self)

    def __getattribute__(self, __name: str) -> Any:
        try:
            return object.__getattribute__(self, __name)
        except AttributeError:
            pass
        v = getattr(self.query, __name, None)
        if v is not None:
            return v
        raise AttributeError(__name)

    @classmethod
    def commit(cls):
        cls.session.commit()


def make_model_base(session: Union[scoped_session, sessionmaker]) -> Type[ModelBase]:
    s = scoped_session(session) if isinstance(session, sessionmaker) else session

    class __Base(ModelBase):
        session = s
        query = session.query_property()

    return __Base
