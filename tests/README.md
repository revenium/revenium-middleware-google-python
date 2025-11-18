# Test Suite

## Structure

- Unit tests (provider detection, model names, tokens, URLs, streaming, errors, config)
- E2E tests (real API validation)

## Run Tests

```bash
# Unit tests only
pytest tests/ -v -m "not e2e"

# All tests including E2E
pytest tests/ -v -m e2e

# With coverage
pytest tests/ --cov=revenium_middleware_google --cov-report=html
```

## E2E Requirements

```bash
export REVENIUM_METERING_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"              # For Google AI SDK
export GOOGLE_CLOUD_PROJECT="your-project"    # For Vertex AI SDK
```

## Verify E2E Results

After E2E tests, search Revenium dashboard for trace IDs printed in test output.
