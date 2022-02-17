def _get_flask_adapter():
    from .flaskadapter import FlaskAdapter

    return FlaskAdapter


FlaskAdapter = _get_flask_adapter()

__all__ = ["FlaskAdapter"]
