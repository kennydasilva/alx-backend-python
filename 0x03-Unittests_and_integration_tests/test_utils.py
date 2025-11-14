#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""

import json
import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch

from utils import access_nested_map
from utils import get_json
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns expected values.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """
        Test that access_nested_map raises KeyError on missing keys.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertIn(missing_key, str(context.exception))


class TestGetJson(unittest.TestCase):
    """
    Test cases for the get_json function.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.urllib.request.urlopen")
    def test_get_json(self, test_url, test_payload, mock_urlopen):
        """
        Test that get_json returns the expected JSON payload.
        """
        mock_resp = Mock()
        data = json.dumps(test_payload).encode("utf-8")
        mock_resp.read.return_value = data

        mock_urlopen.return_value.__enter__.return_value = mock_resp

        result = get_json(test_url)

        mock_urlopen.assert_called_once_with(
            test_url,
        )
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test cases for the memoize decorator.
    """

    def test_memoize(self):
        """
        Test that memoize caches the returned value of a method.
        """

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        inst = TestClass()

        with patch.object(
            TestClass,
            "a_method",
            return_value=42
        ) as mock_method:
            result1 = inst.a_property
            result2 = inst.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
