#!/usr/bin/env python3
"""
Generic utilities for github org client.
"""

import urllib.request
import json
from functools import wraps
from typing import Mapping, Sequence, Any, Dict, Callable


__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested map using a sequence of keys.
    """
    for key in path:
        if isinstance(nested_map, Mapping) and key in nested_map:
            nested_map = nested_map[key]
        else:
            raise KeyError(key)
    return nested_map


def get_json(url: str) -> Dict:
    """
    Fetch JSON data from a URL.
    """
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))


def memoize(fn: Callable) -> Callable:
    """
    Memoize decorator for class methods.
    """
    attr_name = "_" + fn.__name__

    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)