#!/usr/bin/env python3
"""
Generic utilities for github org client.
"""

import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Dict, Callable


__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested map using a path of keys.

    Example:
        nested_map = {"a": {"b": {"c": 1}}}
        access_nested_map(nested_map, ["a", "b", "c"])  # returns 1
    """
    value = nested_map
    for key in path:
        if not isinstance(value, Mapping):
            raise KeyError(key)
        value = value[key]
    return value


def get_json(url: str) -> Dict:
    """Fetch JSON data from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """
    Memoize decorator for class methods.

    Example:
        class MyClass:
            @memoize
            def a_method(self):
                return 42
    """
    attr_name = "_" + fn.__name__

    @wraps(fn)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(wrapper)
