"""
Copyright (c) 2025 Revenium, Inc.
SPDX-License-Identifier: MIT
"""

"""
Tests for metadata transformation, particularly subscriber object handling.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from revenium_middleware_google.common.types import ProviderMetadata, TokenCounts, OperationType
from revenium_middleware_google.common.utils import meter_usage


class TestMetadataTransformation:
    """Test metadata transformation from flat to nested structures."""

    def setup_method(self):
        """Set up test fixtures."""
        self.provider_metadata = ProviderMetadata.for_google_ai_sdk()
        self.token_counts = TokenCounts(
            input_tokens=100,
            output_tokens=150,
            total_tokens=250,
            cached_tokens=0
        )

    @patch('revenium_middleware_google.common.utils.client')
    def test_nested_subscriber_format(self, mock_client):
        """Test that nested subscriber format is passed through correctly."""
        # Arrange
        mock_client.ai.create_completion = Mock(return_value=Mock(id="test-id"))

        usage_metadata = {
            "subscriber": {
                "id": "user-123",
                "email": "user@example.com",
                "credential": {
                    "name": "api-key-name",
                    "value": "api-key-value"
                }
            },
            "organization_id": "org-456",
            "product_id": "product-789"
        }

        # Act
        meter_usage(
            "gemini-2.0-flash-001",
            self.provider_metadata,
            self.token_counts,
            operation_type=OperationType.CHAT,
            usage_metadata=usage_metadata
        )

        # Assert
        call_args = mock_client.ai.create_completion.call_args
        assert call_args is not None
        completion_args = call_args[1]

        # Verify subscriber object structure
        assert "subscriber" in completion_args
        subscriber = completion_args["subscriber"]
        assert subscriber["id"] == "user-123"
        assert subscriber["email"] == "user@example.com"
        assert "credential" in subscriber
        assert subscriber["credential"]["name"] == "api-key-name"
        assert subscriber["credential"]["value"] == "api-key-value"

    @patch('revenium_middleware_google.common.utils.client')
    @patch('revenium_middleware_google.common.utils.logger')
    def test_flat_keys_backward_compatibility(self, mock_logger, mock_client):
        """Test that flat subscriber keys are transformed to nested structure with deprecation warning."""
        # Arrange
        mock_client.ai.create_completion = Mock(return_value=Mock(id="test-id"))

        usage_metadata = {
            "subscriber_id": "user-123",
            "subscriber_email": "user@example.com",
            "subscriber_credential_name": "api-key-name",
            "subscriber_credential": "api-key-value",
            "organization_id": "org-456"
        }

        # Act
        meter_usage(
            "gemini-2.0-flash-001",
            self.provider_metadata,
            self.token_counts,
            operation_type=OperationType.CHAT,
            usage_metadata=usage_metadata
        )

        # Assert
        call_args = mock_client.ai.create_completion.call_args
        assert call_args is not None
        completion_args = call_args[1]

        # Verify transformation to nested structure
        assert "subscriber" in completion_args
        subscriber = completion_args["subscriber"]
        assert subscriber["id"] == "user-123"
        assert subscriber["email"] == "user@example.com"
        assert "credential" in subscriber
        assert subscriber["credential"]["name"] == "api-key-name"
        assert subscriber["credential"]["value"] == "api-key-value"

        # Verify deprecation warning was logged
        mock_logger.warning.assert_called_once()
        warning_message = mock_logger.warning.call_args[0][0]
        assert "deprecated" in warning_message.lower()
        assert "subscriber_id" in warning_message or "flat" in warning_message.lower()

    @patch('revenium_middleware_google.common.utils.client')
    def test_nested_format_preferred_over_flat(self, mock_client):
        """Test that nested format is preferred when both formats present."""
        # Arrange
        mock_client.ai.create_completion = Mock(return_value=Mock(id="test-id"))

        usage_metadata = {
            # Nested format (should be used)
            "subscriber": {
                "id": "nested-user-123",
                "email": "nested@example.com"
            },
            # Flat format (should be ignored)
            "subscriber_id": "flat-user-456",
            "subscriber_email": "flat@example.com"
        }

        # Act
        meter_usage(
            "gemini-2.0-flash-001",
            self.provider_metadata,
            self.token_counts,
            operation_type=OperationType.CHAT,
            usage_metadata=usage_metadata
        )

        # Assert
        call_args = mock_client.ai.create_completion.call_args
        completion_args = call_args[1]

        # Verify nested format was used
        assert "subscriber" in completion_args
        subscriber = completion_args["subscriber"]
        assert subscriber["id"] == "nested-user-123"
        assert subscriber["email"] == "nested@example.com"

    @patch('revenium_middleware_google.common.utils.client')
    def test_partial_subscriber_data(self, mock_client):
        """Test handling of partial subscriber data."""
        # Arrange
        mock_client.ai.create_completion = Mock(return_value=Mock(id="test-id"))

        usage_metadata = {
            "subscriber": {
                "id": "user-123"
                # email and credential missing
            }
        }

        # Act
        meter_usage(
            "gemini-2.0-flash-001",
            self.provider_metadata,
            self.token_counts,
            operation_type=OperationType.CHAT,
            usage_metadata=usage_metadata
        )

        # Assert
        call_args = mock_client.ai.create_completion.call_args
        completion_args = call_args[1]

        # Verify partial subscriber data is included
        assert "subscriber" in completion_args
        subscriber = completion_args["subscriber"]
        assert subscriber["id"] == "user-123"
        assert "email" not in subscriber or subscriber.get("email") is None

    @patch('revenium_middleware_google.common.utils.client')
    def test_no_subscriber_data(self, mock_client):
        """Test that completion works without subscriber data."""
        # Arrange
        mock_client.ai.create_completion = Mock(return_value=Mock(id="test-id"))

        usage_metadata = {
            "organization_id": "org-456",
            "product_id": "product-789"
        }

        # Act
        meter_usage(
            "gemini-2.0-flash-001",
            self.provider_metadata,
            self.token_counts,
            operation_type=OperationType.CHAT,
            usage_metadata=usage_metadata
        )

        # Assert
        call_args = mock_client.ai.create_completion.call_args
        completion_args = call_args[1]

        # Verify subscriber is not in args if no data provided
        assert "subscriber" not in completion_args

    @patch('revenium_middleware_google.common.utils.client')
    def test_other_metadata_fields(self, mock_client):
        """Test that other metadata fields are preserved correctly."""
        # Arrange
        mock_client.ai.create_completion = Mock(return_value=Mock(id="test-id"))

        usage_metadata = {
            "trace_id": "trace-123",
            "task_type": "document-analysis",
            "organization_id": "org-456",
            "subscription_id": "sub-789",
            "product_id": "product-101",
            "agent": "analyzer-v2",
            "response_quality_score": 0.95
        }

        # Act
        meter_usage(
            "gemini-2.0-flash-001",
            self.provider_metadata,
            self.token_counts,
            operation_type=OperationType.CHAT,
            usage_metadata=usage_metadata
        )

        # Assert
        call_args = mock_client.ai.create_completion.call_args
        completion_args = call_args[1]

        # Verify all metadata fields are preserved
        assert completion_args["trace_id"] == "trace-123"
        assert completion_args["task_type"] == "document-analysis"
        assert completion_args["organization_id"] == "org-456"
        assert completion_args["subscription_id"] == "sub-789"
        assert completion_args["product_id"] == "product-101"
        assert completion_args["agent"] == "analyzer-v2"
        assert completion_args["response_quality_score"] == 0.95
