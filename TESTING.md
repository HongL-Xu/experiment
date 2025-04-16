# Testing Instructions

This project includes both Python (backend) and JavaScript (frontend) tests.

## Python Tests

The Python tests use the built-in `unittest` framework and test the Flask API endpoints.

### Setup
1. Make sure you have all required Python packages installed:
```bash
pip install -r requirements.txt
```

### Running Python Tests
To run the Python tests, execute:
```bash
python -m unittest Unit_tests/test_app.py
```

The tests cover:
- Adding new donations
- Filtering donations by year
- Deleting donations

## JavaScript Tests

The JavaScript tests use Jest and test the frontend functionality.

### Setup
1. Install Node.js dependencies:
```bash
npm install
```

### Running JavaScript Tests
To run the JavaScript tests, execute:
```bash
npm test
```

The tests cover:
- Table rendering with mock data
- Year filter functionality

## Test Structure

### Python Tests (`Unit_tests/test_app.py`)
- `TestDonationsApp` class contains all API tests
- Uses a temporary SQLite database for testing
- Automatically cleans up after tests

### JavaScript Tests (`Unit_tests/test_app.test.js`)
- Uses Jest's JSDOM environment
- Mocks the DOM for testing
- Tests frontend components in isolation

## Continuous Integration

To run all tests in a CI environment:
```bash
# Run Python tests
python -m unittest discover Unit_tests

# Run JavaScript tests
npm test
``` 