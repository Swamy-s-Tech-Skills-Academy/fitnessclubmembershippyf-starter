# isort: off
import pytest
import sys
import os
import requests
import time

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the Flask app after path is adjusted
from app import app  # noqa
# isort: on


class TestHTTPResponse:
    """
    Test the HTTP response of the running Flask application.

    Note: This test requires the Flask app to be running on http://127.0.0.1:5000
    Run the app first with: cd src && python app.py
    """

    @pytest.fixture(scope="class")
    def flask_app_url(self):
        """Base URL for the Flask application."""
        return "http://127.0.0.1:5000"

    def test_flask_app_is_running(self, flask_app_url):
        """
        Test that the Flask app is running and returns a 200 status code.
        """
        try:
            # Give a small delay to ensure the app is ready
            time.sleep(1)

            response = requests.get(flask_app_url, timeout=5)

            # Check status code
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

            print(f"✅ Status: {response.status_code}")

        except requests.exceptions.ConnectionError:
            pytest.fail(
                "❌ Could not connect to Flask app. Is it running on http://127.0.0.1:5000?")
        except requests.exceptions.Timeout:
            pytest.fail("❌ Request timed out. Flask app may be unresponsive.")

    def test_flask_app_content(self, flask_app_url):
        """
        Test that the Flask app returns the expected content.
        """
        try:
            time.sleep(1)

            response = requests.get(flask_app_url, timeout=5)

            # Check that the response contains the expected text
            expected_text = "Welcome to Fitness Club"
            assert expected_text in response.text, f"Expected '{expected_text}' in response content"

            print("✅ Flask app working! Content validation passed.")

        except requests.exceptions.ConnectionError:
            pytest.fail(
                "❌ Could not connect to Flask app. Is it running on http://127.0.0.1:5000?")
        except requests.exceptions.Timeout:
            pytest.fail("❌ Request timed out. Flask app may be unresponsive.")

    def test_flask_app_response_time(self, flask_app_url):
        """
        Test that the Flask app responds within a reasonable time.
        """
        try:
            start_time = time.time()
            response = requests.get(flask_app_url, timeout=10)
            end_time = time.time()

            response_time = end_time - start_time

            # Assert response time is reasonable (less than 2 seconds)
            assert response_time < 2.0, f"Response time too slow: {response_time:.2f}s"

            print(f"✅ Response time: {response_time:.2f}s")

        except requests.exceptions.ConnectionError:
            pytest.fail(
                "❌ Could not connect to Flask app. Is it running on http://127.0.0.1:5000?")
        except requests.exceptions.Timeout:
            pytest.fail("❌ Request timed out. Flask app may be unresponsive.")


if __name__ == "__main__":
    """
    Allow running this test file directly for quick validation.

    Usage:
    python tests/test_http_response.py
    """
    print("🧪 Running HTTP Response Tests...")
    print("📋 Note: Make sure Flask app is running on http://127.0.0.1:5000")
    print("   Run: cd src && python app.py")
    print("-" * 50)

    # Run the tests programmatically
    pytest.main([__file__, "-v", "--tb=short"])
