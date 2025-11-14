#!/usr/bin/env python3
"""
Unit tests for the utils module
"""

import unittest
import json
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertIn(missing_key, str(context.exception))


class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.urllib.request.urlopen")
    def test_get_json(self, test_url, test_payload, mock_urlopen):
        mock_response = Mock()
        json_data = json.dumps(test_payload).encode("utf-8")
        mock_response.read.return_value = json_data

        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = get_json(test_url)

        mock_urlopen.assert_called_once_with(
            test_url,
        )

        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator"""

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
