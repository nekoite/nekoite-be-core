# Nekoite Backend Core

[![pypi](https://img.shields.io/pypi/v/nekoite-be-core)][pypi-url]
[![build](https://github.com/nekoite/nekoite-be-core/actions/workflows/build.yml/badge.svg)][github-build-url]

[pypi-url]: https://pypi.org/project/nekoite-be-core/
[github-build-url]: https://github.com/nekoite/nekoite-be-core/actions/workflows/build.yml

## Usage

Requires python 3.7 or newer.

```text
pip install nekoite-be-core
```

There are some [examples](examples/) to look at.

Basically, choose an adapter (or build on your own), create
some views and routes, and give it to the function `register_routes`.

```python
routes = {"/a": AView, ...}
adapter = SomeAdapter(*args)
register_routes(adapter, routes)
```

## Modules

### View

Extend the class `ViewBase`. Override the function `handle_req`.
You can specify the `request_schema` and `response_schema`, and if they
are not specified or `None`, then the request or response format will
not be checked. `method` can be a string or list of strings indicating
the HTTP methods accepted by this view.

```python
class TestView(ViewBase):
    request_schema = {"id": fields.Integer(required=True)}
    response_schema = {"id": fields.Integer(), "timestamp": fields.Integer()}
    methods = ["GET", "POST"]

    def handle_req(self, req: t.Dict[str, t.Any]) -> t.Any:
        return {
            "id": req["id"],
            "timestamp": int(time()),
        }
```

### Fields

You can import `fields` from this package. It includes some field type
defined in `marshmallow`, and the `Nested` type is rewritten to accept dict
as parameter.

The detailed usage of the types in `fields` can be found on
[the homepage of marshmallow][marshmallow-hp].

```python
from nekoite_be_core import fields

# ...
request_schema = {
    "id": fields.Integer(required=True),
    ...
}
```

[marshmallow-hp]: https://marshmallow.readthedocs.io/en/stable/index.html
