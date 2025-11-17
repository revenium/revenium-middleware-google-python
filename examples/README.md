# Revenium Google AI Middleware - Examples

This directory contains working examples demonstrating how to use the Revenium middleware with Google AI services.

## Getting Started - Step by Step

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# For Google AI SDK (Gemini Developer API)
pip install "revenium-middleware-google[genai]"

# For Vertex AI SDK (Google Cloud)
pip install "revenium-middleware-google[vertex]"

# For both SDKs
pip install "revenium-middleware-google[all]"
```

### 3. Environment Setup

Create a `.env` file or export environment variables:

**For Google AI SDK:**
```bash
export REVENIUM_METERING_API_KEY="your-revenium-api-key"
export GOOGLE_API_KEY="your-google-api-key"
```

**For Vertex AI SDK:**
```bash
export REVENIUM_METERING_API_KEY="your-revenium-api-key"
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"  # optional

# Authenticate with Google Cloud
gcloud auth application-default login
```

### 4. Run Examples

```bash
# Simple getting started examples
python examples/getting_started_google_ai.py
python examples/getting_started_vertex_ai.py

# Comprehensive test suite
python examples/simple_test.py --provider google-ai
python examples/simple_test.py --provider vertex-ai
```

---

## Which SDK Should I Choose?

| Use Case | Recommended SDK | Why |
|----------|----------------|-----|
| **Quick prototyping** | Google AI SDK | Simple API key setup, but does NOT support token counts on embeddings |
| **Production applications** | Vertex AI SDK | Full token counting, enterprise features |
| **Embeddings-heavy workloads** | Vertex AI SDK | Complete token tracking for embeddings |
| **Enterprise/GCP environments** | Vertex AI SDK | Advanced Google Cloud integration |
| **Simple chat applications** | Either SDK | Both provide full chat support |

**Recommendation**: Use Vertex AI SDK for production applications that need comprehensive token counting and advanced features.

---

## Available Examples

### `getting_started_google_ai.py` - Simple Google AI SDK Entry Point

The simplest possible example for Google AI SDK (Gemini Developer API).

**What it demonstrates:**
- Zero-config integration (just import the middleware)
- Single chat completion
- Automatic usage tracking

**Run it:**
```bash
python examples/getting_started_google_ai.py
```

---

### `getting_started_vertex_ai.py` - Simple Vertex AI SDK Entry Point

The simplest possible example for Vertex AI SDK (Google Cloud).

**What it demonstrates:**
- Zero-config integration
- Vertex AI initialization
- Single chat completion
- Automatic usage tracking

**Run it:**
```bash
python examples/getting_started_vertex_ai.py
```

---

### `simple_test.py` - Comprehensive Test Suite

Full-featured test suite with multiple scenarios and provider selection.

**What it demonstrates:**
- Provider selection (Google AI vs Vertex AI)
- Zero-config and enhanced tracking examples
- Environment validation
- Error handling and debugging
- Command-line arguments

**Run it:**
```bash
# Test Google AI SDK
python examples/simple_test.py --provider google-ai

# Test Vertex AI SDK
python examples/simple_test.py --provider vertex-ai

# Show help
python examples/simple_test.py --help
```

---

### `simple_streaming_test.py` - Streaming Responses

Demonstrates streaming responses with real-time token counting.

**What it demonstrates:**
- Streaming chat completions
- Time-to-first-token tracking
- Streaming with both SDKs
- Metadata tracking with streaming

**Run it:**
```bash
python examples/simple_streaming_test.py --provider google-ai
python examples/simple_streaming_test.py --provider vertex-ai
```

---

### `simple_embeddings_test.py` - Text Embeddings

Demonstrates text embeddings with token counting.

**What it demonstrates:**
- Text embeddings generation
- Token counting for embeddings (Vertex AI)
- Batch embeddings processing
- SDK differences

**Run it:**
```bash
python examples/simple_embeddings_test.py --provider google-ai
python examples/simple_embeddings_test.py --provider vertex-ai
```

**Note:** Google AI SDK embeddings don't return token counts due to API limitations. Use Vertex AI SDK for full token tracking.

---

## Configuration

Configure the middleware using environment variables:

### Required Environment Variables

#### For Google AI SDK (Gemini Developer API)
```bash
# Required
export REVENIUM_METERING_API_KEY=your_revenium_api_key
export GOOGLE_API_KEY=your_google_api_key

# Optional: Revenium base URL (defaults to production)
export REVENIUM_METERING_BASE_URL=https://api.revenium.ai
export REVENIUM_LOG_LEVEL=INFO
```

#### For Vertex AI SDK (Google Cloud)
```bash
# Required
export REVENIUM_METERING_API_KEY=your_revenium_api_key
export GOOGLE_CLOUD_PROJECT=your_gcp_project_id

# Recommended
export GOOGLE_CLOUD_LOCATION=us-central1

# Google Cloud Authentication (choose one)
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
# OR use: gcloud auth application-default login

# Optional: Revenium base URL (defaults to production)
export REVENIUM_METERING_BASE_URL=https://api.revenium.ai
export REVENIUM_LOG_LEVEL=INFO
```

### Using .env File

Create a `.env` file in your project root:

```bash
# Required for all configurations
REVENIUM_METERING_API_KEY=your_revenium_api_key

# For Google AI SDK
GOOGLE_API_KEY=your_google_api_key

# For Vertex AI SDK
GOOGLE_CLOUD_PROJECT=your_gcp_project_id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Optional settings
REVENIUM_METERING_BASE_URL=https://api.revenium.ai
REVENIUM_LOG_LEVEL=DEBUG
```

### Google Cloud Authentication

The Vertex AI SDK uses the standard Google Cloud authentication chain:

1. **Service Account Key File** (recommended for production):
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
   ```

2. **Application Default Credentials** (for development):
   ```bash
   gcloud auth application-default login
   ```

3. **Compute Engine/GKE Service Account** (automatic in GCP environments)

4. **Environment Variables**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
   ```

Ensure your credentials have the following permissions:
- `aiplatform.endpoints.predict`
- `ml.projects.predict` (for some models)

### Configuration Variables

| Variable | Required | SDK | Description |
|----------|----------|-----|-------------|
| `REVENIUM_METERING_API_KEY` | Yes | Both | Your Revenium API key |
| `GOOGLE_API_KEY` | Yes | Google AI | Google AI API key (Gemini Developer API) |
| `GOOGLE_CLOUD_PROJECT` | Yes | Vertex AI | Google Cloud project ID |
| `GOOGLE_CLOUD_LOCATION` | No | Vertex AI | Google Cloud location (default: `us-central1`) |
| `GOOGLE_APPLICATION_CREDENTIALS` | No | Vertex AI | Path to service account key file |
| `REVENIUM_METERING_BASE_URL` | No | Both | Revenium API base URL |
| `REVENIUM_LOG_LEVEL` | No | Both | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

---

## Advanced Features

### SDK-Specific Integration

#### Automatic Provider Detection

The middleware automatically chooses between Google AI SDK and Vertex AI SDK:

| Detection Method | When Used | Example |
|-----------------|-----------|---------|
| **Google AI SDK** | When `google.genai` is imported and used | `from google import genai` |
| **Vertex AI SDK** | When `vertexai` is imported and used | `import vertexai` |
| **Dual Support** | When both SDKs are available | Automatic routing based on usage |

**Key Point**: Both SDKs report as "Google" provider for unified analytics and consistent reporting.

**See `getting_started_google_ai.py`** and **`getting_started_vertex_ai.py`** for complete working examples of both SDKs.

### Streaming Support

The middleware supports streaming responses for both SDKs with automatic usage tracking.

**For complete streaming examples, see `simple_streaming_test.py`**

**Key features:**

- Real-time token counting
- Time-to-first-token tracking
- Automatic usage logging when stream completes
- Works with both Google AI SDK and Vertex AI SDK

### Text Embeddings

The middleware supports text embeddings with both SDKs. **Note:** Google AI SDK embeddings don't return token counts due to API limitations. Use Vertex AI SDK for full token tracking.

**For complete embeddings examples, see `simple_embeddings_test.py`**

**SDK Comparison:**

| Feature | Google AI SDK | Vertex AI SDK |
|---------|---------------|---------------|
| **Embeddings Generation** | Full support | Full support |
| **Token Counting** | No tokens (API limitation) | Full token counting |
| **Usage Tracking** | Requests tracked | Full tracking |

---

## Testing Your Setup

The middleware includes comprehensive test scripts to verify your configuration and ensure everything is working correctly. Each test script supports both Google AI SDK and Vertex AI SDK with intelligent provider selection.

### Quick Test Commands

```bash
# Test Google AI SDK (default)
python examples/simple_test.py

# Test Vertex AI SDK
python examples/simple_test.py --provider vertex-ai

# Test streaming functionality
python examples/simple_streaming_test.py --provider google-ai
python examples/simple_streaming_test.py --provider vertex-ai

# Test embeddings (Vertex AI recommended for full token counting)
python examples/simple_embeddings_test.py --provider vertex-ai

# Get help for any test script
python examples/simple_test.py --help
```

### Environment Setup for Testing

#### For Google AI SDK Testing
```bash
export GOOGLE_API_KEY=your_google_api_key
export REVENIUM_METERING_API_KEY=your_revenium_key

# Run the test
python examples/simple_test.py --provider google-ai
```

#### For Vertex AI SDK Testing
```bash
export GOOGLE_CLOUD_PROJECT=your_project_id
export GOOGLE_CLOUD_LOCATION=us-central1  # optional, defaults to us-central1
export REVENIUM_METERING_API_KEY=your_revenium_key

# Ensure Google Cloud authentication
gcloud auth application-default login

# Run the test
python examples/simple_test.py --provider vertex-ai
```

### Expected Test Results

**Successful Test Output:**
```
Revenium Google AI Middleware - Test Suite
Testing: GOOGLE AI SDK
======================================================================
Google API Key: AIzaSyB8oD...
Revenium Key: hak_6PVMBR...

GOOGLE AI SDK EXAMPLES
======================================================================
Google AI SDK detected

Google AI SDK - Basic Example
==================================================
Response: According to the supercomputer Deep Thought...
Tokens: 12 input + 421 output = 433 total
Zero-config integration successful!

Google AI SDK - Enhanced Tracking Example
==================================================
Response: Okay, I'm ready to analyze the quarterly report...
Enhanced metadata tracking enabled!

======================================================================
TEST RESULTS SUMMARY
======================================================================
PASS: google_ai_basic
PASS: google_ai_enhanced

Overall: 2/2 tests passed
Success! Check your Revenium dashboard for usage data
```

**Failed Test Output:**
```
Missing required environment variable for Google AI SDK
   GOOGLE_API_KEY not found

Setup Instructions:
   1. Get your API key from: https://aistudio.google.com/app/apikey
   2. Set the environment variable:
      export GOOGLE_API_KEY=your_google_api_key
   3. Run the test again
```

### Test Script Features

- **Intelligent Provider Selection**: Automatically tests only the selected provider
- **Environment Validation**: Checks for required environment variables before testing
- **Clear Error Messages**: Provides specific setup instructions when configuration is missing
- **Comprehensive Coverage**: Tests basic functionality, enhanced metadata, streaming, and embeddings
- **User-Friendly Output**: Color-coded results with clear success/failure indicators

### Available Test Scripts

| Script | Purpose | Key Features |
|--------|---------|--------------|
| `simple_test.py` | Basic functionality testing | Chat completion, metadata tracking |
| `simple_streaming_test.py` | Streaming functionality | Real-time token counting, streaming responses |
| `simple_embeddings_test.py` | Embeddings testing | Text embeddings, token counting (Vertex AI) |

All test scripts support the `--provider` flag to specify which SDK to test.

---

## Troubleshooting

### Import Errors

```bash
# Ensure correct dependencies are installed
pip install "revenium-middleware-google[all]"
```

### Environment Variables Not Set

```bash
# Verify environment variables
echo $REVENIUM_METERING_API_KEY
echo $GOOGLE_API_KEY
echo $GOOGLE_CLOUD_PROJECT
```

### Vertex AI Authentication Errors

```bash
# Authenticate with Google Cloud
gcloud auth application-default login

# Verify authentication
gcloud auth application-default print-access-token
```

### Debug Mode

Enable debug logging to see detailed middleware activity:

```bash
export REVENIUM_LOG_LEVEL=DEBUG
python examples/getting_started_google_ai.py
```

---

## Requirements

- Python 3.9+
- Revenium API key (sign up at [revenium.ai](https://revenium.ai))
- Google AI API key (for Google AI SDK) or Google Cloud project (for Vertex AI SDK)

---

## Additional Resources

- **Main Documentation:** [README.md](../README.md)
- **Revenium API:** [API Documentation](https://revenium.readme.io/reference/meter_ai_completion)
- **Google AI SDK:** [Google AI Python SDK](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)
- **Vertex AI SDK:** [Vertex AI Python SDK](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk)
