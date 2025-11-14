# Unittests and Integration Tests

This project contains unit tests and integration tests for Python functions.

## Project Structure

- `test_utils.py`: Unit tests for utility functions
- `test_client.py`: Tests for API client (with mocking)
- `utils.py`: Utility functions
- `client.py`: API client implementation
- `fixtures.py`: Test data and fixtures

## Running Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest test_utils.py

# Run with verbose output
python -m unittest discover -v
