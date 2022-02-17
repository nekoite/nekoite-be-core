from typing import Any, List


def unify_to_list(item: Any) -> List:
    if isinstance(item, (tuple, list)):
        return list(item)
    return [item]
