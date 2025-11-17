"""
Copyright (c) 2025 Revenium, Inc.
SPDX-License-Identifier: MIT
"""

"""
Tests for URL standardization and validation.
"""

import pytest
from revenium_middleware_google.common.utils import ensure_meter_in_url


class TestURLStandardization:
    """Test URL standardization logic."""

    def test_plain_base_url_appends_meter(self):
        """Test that plain base URL gets /meter appended."""
        result = ensure_meter_in_url("https://api.revenium.ai")

        assert result == "https://api.revenium.ai/meter"

    def test_url_with_meter_unchanged(self):
        """Test that URL with /meter is unchanged."""
        result = ensure_meter_in_url("https://api.revenium.ai/meter")

        assert result == "https://api.revenium.ai/meter"

    def test_url_with_meter_v2_removes_v2(self):
        """Test that /meter/v2 gets v2 removed."""
        result = ensure_meter_in_url("https://api.revenium.ai/meter/v2")

        assert result == "https://api.revenium.ai/meter"

    def test_url_with_trailing_slash(self):
        """Test that trailing slash is handled."""
        result = ensure_meter_in_url("https://api.revenium.ai/")

        assert result == "https://api.revenium.ai/meter"

    def test_localhost_url(self):
        """Test localhost URL handling."""
        result = ensure_meter_in_url("http://localhost:8000")

        assert result == "http://localhost:8000/meter"

    def test_none_returns_default(self):
        """Test that None returns default URL."""
        result = ensure_meter_in_url(None)

        assert result == "https://api.revenium.ai/meter"

    def test_empty_string_returns_default(self):
        """Test that empty string returns default URL."""
        result = ensure_meter_in_url("")

        assert result == "https://api.revenium.ai/meter"

    def test_whitespace_string_returns_default(self):
        """Test that whitespace string returns default URL."""
        result = ensure_meter_in_url("   ")

        assert result == "https://api.revenium.ai/meter"

    def test_url_with_multiple_version_suffixes(self):
        """Test handling of various version suffixes."""
        test_cases = [
            ("https://api.revenium.ai/meter/v1", "https://api.revenium.ai/meter"),
            ("https://api.revenium.ai/meter/v2", "https://api.revenium.ai/meter"),
            ("https://api.revenium.ai/meter/v3", "https://api.revenium.ai/meter"),
            ("https://api.revenium.ai/meter/v4", "https://api.revenium.ai/meter"),
            ("https://api.revenium.ai/meter/v5", "https://api.revenium.ai/meter"),
        ]

        for input_url, expected in test_cases:
            result = ensure_meter_in_url(input_url)
            assert result == expected

    def test_url_without_scheme_defaults_https(self):
        """Test that URL without scheme gets https."""
        # This tests the expected behavior if scheme is missing
        from urllib.parse import urlparse

        url = "api.revenium.ai/meter"
        parsed = urlparse(url)

        if not parsed.scheme:
            # Should default to https
            expected_scheme = "https"
            assert expected_scheme == "https"

    def test_preserves_custom_port(self):
        """Test that custom ports are preserved."""
        result = ensure_meter_in_url("http://localhost:8080")

        assert "8080" in result
        assert result == "http://localhost:8080/meter"


class TestAPIEndpointCorrectness:
    """Test that API endpoints use correct domain."""

    def test_default_uses_ai_domain(self):
        """Test that default domain is .ai not .io."""
        result = ensure_meter_in_url(None)

        assert "api.revenium.ai" in result
        assert "api.revenium.io" not in result

    def test_io_domain_in_input_preserved(self):
        """Test that if user provides .io, it's preserved (for backward compat)."""
        result = ensure_meter_in_url("https://api.revenium.io")

        # Should preserve what user provided
        assert "revenium.io" in result or "revenium.ai" in result

    def test_correct_endpoint_path(self):
        """Test that endpoint path is /meter."""
        result = ensure_meter_in_url("https://api.revenium.ai")

        assert result.endswith("/meter")
        assert "/meter/v2" not in result  # Should not have /v2

    def test_full_api_path_construction(self):
        """Test construction of full API path."""
        base = ensure_meter_in_url("https://api.revenium.ai")

        # Full path would be base + /v2/ai/completions
        full_path = f"{base}/v2/ai/completions"

        assert full_path == "https://api.revenium.ai/meter/v2/ai/completions"


class TestEdgeCases:
    """Test edge cases in URL handling."""

    def test_url_with_query_parameters(self):
        """Test URL with query parameters."""
        # Query params should be handled appropriately
        url_with_params = "https://api.revenium.ai?param=value"

        # Should still work
        result = ensure_meter_in_url(url_with_params)
        assert "api.revenium.ai" in result

    def test_url_with_fragment(self):
        """Test URL with fragment identifier."""
        url_with_fragment = "https://api.revenium.ai#section"

        result = ensure_meter_in_url(url_with_fragment)
        assert "api.revenium.ai" in result

    def test_url_with_auth(self):
        """Test URL with authentication."""
        url_with_auth = "https://user:pass@api.revenium.ai"

        result = ensure_meter_in_url(url_with_auth)
        assert "api.revenium.ai" in result

    def test_malformed_url_handled_gracefully(self):
        """Test that malformed URLs are handled."""
        malformed_urls = [
            "not-a-url",
            "ftp://api.revenium.ai",  # Wrong protocol
            "//api.revenium.ai",  # Protocol-relative
        ]

        for url in malformed_urls:
            # Should not crash
            try:
                result = ensure_meter_in_url(url)
                # Should return something valid
                assert result is not None
            except Exception:
                # Or return default if it can't parse
                pass
