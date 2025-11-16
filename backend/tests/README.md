# OLP 2025 Backend Test Suite

This directory contains comprehensive unit and integration tests for the OLP 2025 backend service.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Test configuration and shared fixtures
├── test_utils.py                  # Test utilities and helper functions
├── test_base_service.py           # Unit tests for BaseService
├── test_building_service.py       # Unit tests for BuildingService
├── test_air_quality_service.py    # Unit tests for AirQualityService
├── test_other_services.py         # Unit tests for remaining services
├── test_models.py                 # Unit tests for Pydantic models
├── test_building_router_integration.py  # Integration tests for API endpoints
├── test_model.py                  # Legacy test file (deprecated)
└── run_tests.py                   # Test runner script
```

## Test Categories

### Unit Tests

- **Service Layer Tests**: Test individual service classes in isolation
- **Model Tests**: Test Pydantic model validation and serialization
- **Utility Tests**: Test helper functions and utilities

### Integration Tests

- **API Router Tests**: Test FastAPI endpoints with mocked services
- **End-to-End Scenarios**: Test complete request-response cycles

## Running Tests

### Quick Test Run

```bash
# From the backend directory
./run_tests.py
```

### Manual Test Execution

#### Run all tests

```bash
pytest tests/ -v --tb=short
```

#### Run with coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
```

#### Run specific test file

```bash
pytest tests/test_building_service.py -v
```

#### Run only integration tests

```bash
pytest tests/test_*_integration.py -v
```

#### Run only unit tests

```bash
pytest tests/test_*.py -v --ignore=tests/test_*_integration.py
```

### Development Workflow

#### Before committing

```bash
# Run linting
ruff check .

# Run type checking
mypy app

# Run tests with coverage
pytest tests/ --cov=app --cov-fail-under=80
```

#### Watch mode for development

```bash
pytest tests/ -v -f
```

## Test Coverage

The test suite aims for >80% code coverage. Coverage reports are generated in:

- Terminal output (summary)
- `htmlcov/index.html` (detailed HTML report)
- `coverage.xml` (XML format for CI/CD)

## Test Configuration

### Fixtures (conftest.py)

- `client`: FastAPI test client
- `mock_base_service`: Mocked BaseService instance
- Sample data fixtures for all entity types
- HTTP response mocking utilities

### Test Utilities (test_utils.py)

- NGSI-LD entity builders
- Mock HTTP response creators
- Validation helpers
- Common test data generators

## Testing Patterns

### Service Layer Tests

```python
@pytest.mark.asyncio
async def test_service_method_success(self, service):
    # Setup mocks
    service._client = AsyncMock()
    service._client.request.return_value.json.return_value = mock_data

    # Execute method
    result = await service.method_under_test()

    # Assertions
    assert result == expected_data
    service._client.request.assert_called_once()
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_api_endpoint_success(self, client):
    with patch('app.services.building_service.building_service') as mock_service:
        mock_service.method.return_value = mock_data

        response = await client.get("/api/v1/buildings/")

        assert response.status_code == 200
        assert response.json() == mock_data
```

## Mock Strategy

### HTTP Client Mocking

- Service layer tests mock HTTPX AsyncClient
- All HTTP requests are intercepted and return predefined responses
- Error conditions are tested by raising appropriate exceptions

### Service Mocking

- Integration tests mock service instances
- FastAPI dependency injection is patched with mock objects
- Real business logic is not executed in integration tests

## Test Data Management

### Fixtures provide:

- Valid sample data for all entity types
- Invalid data for negative testing
- Edge cases for boundary testing

### Data helpers:

- NGSI-LD compliant entity builders
- Attribute structure creators
- Validation utilities

## Error Testing

### Service Layer

- HTTP status errors (404, 409, 500, etc.)
- Connection errors and timeouts
- Validation errors and malformed responses

### API Layer

- Request validation errors (422)
- Service unavailable errors (503)
- Authentication/authorization (if implemented)

## Environment Variables

Tests use environment variables for configuration:

```bash
# Orion-LD broker URL (default: http://fiware-orionld:1026/ngsi-ld/v1)
export ORION_LD_URL=http://localhost:1026/ngsi-ld/v1

# JSON-LD context URL (default: http://context/datamodels.context-ngsi.jsonld)
export CONTEXT_URL=http://localhost/context.jsonld
```

## Continuous Integration

The test suite is designed for CI/CD pipelines:

```bash
# CI pipeline command
./run_tests.py
```

This command:

1. Installs dependencies
2. Runs linting (ruff)
3. Runs type checking (mypy)
4. Runs all tests with coverage
5. Fails if coverage < 80%

## Best Practices

1. **One assertion per test** when possible
2. **Descriptive test names** that explain the scenario
3. **Arrange-Act-Assert** pattern
4. **Mock external dependencies** (HTTP clients, databases)
5. **Test both happy path and error conditions**
6. **Use fixtures for common test data**
7. **Keep tests isolated** - don't depend on test execution order
8. **Clean up resources** in async context managers

## Adding New Tests

1. Create test file in appropriate category
2. Use existing fixtures when possible
3. Follow established patterns and naming conventions
4. Add coverage for new code paths
5. Update this README if adding new test categories

## Troubleshooting

### Common Issues

**Tests fail due to missing dependencies:**

```bash
pip install -r requirements-dev.txt
```

**Coverage not generated:**

```bash
pip install pytest-cov
```

**Import errors:**

- Ensure PYTHONPATH includes the project root
- Run tests from the backend directory
- Check conftest.py is in the tests directory

**Async test issues:**

- Use `@pytest.mark.asyncio` decorator
- Ensure test functions are `async def`
- Check that event loop is properly configured

### Getting Help

- Check pytest documentation: https://docs.pytest.org/
- Review FastAPI testing guide: https://fastapi.tiangolo.com/tutorial/testing/
- Examine existing tests for patterns and examples
