from typing import Any, Optional

from sigla.data.data import Data
from sigla.data.errors import DataKeyError


def get_default_value_for_attribute(data: Data, field: str) -> Optional[Any]:
    """
    Get value for attribute ignoring DataKeyErrors. If error raises, value is
    None
    """
    try:
        value = getattr(data, field, None)
    except DataKeyError:
        value = None
    return value
