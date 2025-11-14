#!/usr/bin/env python3
"""
Unit tests for the utils module
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for the access_nested_map function
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected result
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """
        Test that access_nested_map raises KeyError for invalid paths
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertIn(missing_key, str(context.exception))


class TestGetJson(unittest.TestCase):
    """
    Test cases for the get_json function
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns the expected result
        without making HTTP calls
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch('utils.requests.get',
                   return_value=mock_response) as mock_get:

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test cases for the memoize decorator
    """

    def test_memoize(self):
        """
        Test that memoize caches result and calls the method only once
        """

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Patch a_method BEFORE instantiating TestClass
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:

            test_instance = TestClass()

            result1 = test_instance.a_property()
            result2 = test_instance.a_property()

            # Both calls must return the same memoized value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was only called once
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()

