#!/usr/bin/env python3
"""
Unit tests for the client module
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for the GithubOrgClient class
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        """
        # Set up the mock return value
        expected_response = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_response
        
        # Create client instance
        client = GithubOrgClient(org_name)
        
        # Call the org property
        result = client.org
        
        # Verify get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        
        # Verify the result matches expected response
        self.assertEqual(result, expected_response)
        
        # Verify get_json was not executed (it was mocked)
        # This is implicit in the mock setup


if __name__ == '__main__':
    unittest.main()