from typing import Any, List

__all__ = ["unify_to_list"]


def unify_to_list(item: Any) -> List:
    if isinstance(item, (tuple, list)):
        return list(item)
    return [item]
