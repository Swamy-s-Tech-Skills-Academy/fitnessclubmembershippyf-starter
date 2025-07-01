# isort: off
import pytest
import sys
import os
import requests
import time
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the Flask app after path is adjusted
from app import app  # noqa
# isort: on


class TestFlaskAppRunning:
    """
    Test suite to verify the Flask app is running and responding correctly.

    This test assumes that the Flask app is already running on http://127.0.0.1:5000
    (started manually with `python src/app.py` or similar).
    """

    BASE_URL = "http://127.0.0.1:5000"
    EXPECTED_CONTENT = "Welcome to Fitness Club"
    TIMEOUT_SECONDS = 10

    def test_flask_app_is_running(self):
        """
        Test that the Flask app is running and accessible via HTTP.

        This test will:
        1. Wait a moment for the server to be ready
        2. Send a GET request to the home page
        3. Verify the response status is 200
        4. Verify the expected content is present
        """
        # Give the server a moment to be ready
        time.sleep(2)

        try:
            response = requests.get(
                self.BASE_URL,
                timeout=self.TIMEOUT_SECONDS
            )

            # Check status code
            assert response.status_code == 200, (
                f"Expected status 200, got {response.status_code}. "
                f"Make sure Flask app is running on {self.BASE_URL}"
            )

            # Check content
            assert self.EXPECTED_CONTENT in response.text, (
                f"Expected '{self.EXPECTED_CONTENT}' in response. "
                f"Got: {response.text[:200]}..."
            )

            print(f"✅ Flask app is running successfully!")
            print(f"   Status: {response.status_code}")
            print(f"   Content check: '{self.EXPECTED_CONTENT}' found")

        except requests.exceptions.ConnectionError:
            pytest.fail(
                f"❌ Could not connect to {self.BASE_URL}. "
                f"Make sure the Flask app is running with: python src/app.py"
            )
        except requests.exceptions.Timeout:
            pytest.fail(
                f"❌ Request to {self.BASE_URL} timed out after {self.TIMEOUT_SECONDS}s"
            )

    def test_flask_app_response_time(self):
        """
        Test that the Flask app responds within a reasonable time.
        """
        start_time = time.time()

        try:
            response = requests.get(
                self.BASE_URL,
                timeout=self.TIMEOUT_SECONDS
            )

            response_time = time.time() - start_time

            # Should respond within 5 seconds
            assert response_time < 5.0, (
                f"Response took too long: {response_time:.2f}s"
            )

            print(f"✅ Response time: {response_time:.3f}s")

        except requests.exceptions.ConnectionError:
            pytest.skip(
                f"Flask app not running on {self.BASE_URL}, skipping response time test"
            )


def check_flask_app_manual() -> Optional[str]:
    """
    Manual check function that can be called directly.
    Returns success message or None if failed.
    """
    try:
        time.sleep(2)
        response = requests.get("http://127.0.0.1:5000", timeout=10)

        if response.status_code == 200 and "Welcome to Fitness Club" in response.text:
            return f"✅ Flask app working! Status: {response.status_code}"
        else:
            return f"❌ Issue detected. Status: {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "❌ Could not connect. Make sure Flask app is running."
    except Exception as e:
        return f"❌ Error: {str(e)}"


if __name__ == "__main__":
    """
    Allow running this test file directly for quick validation.

    Usage:
        python tests/test_flask_app_running.py
    """
    print("🔍 Checking if Flask app is running...")
    result = check_flask_app_manual()
    print(result)

    if "✅" in result:
        print("\n🚀 You can also run this as a pytest:")
        print("   pytest tests/test_flask_app_running.py -v")
    else:
        print("\n💡 To start the Flask app:")
        print("   cd src")
        print("   python app.py")
