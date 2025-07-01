# isort: off
import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the Flask app after adding src to path
from app import app  # noqa
# isort: on


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Fitness Club" in response.data


def test_flask_app_running():
    """Test that Flask app is properly configured"""
    assert app is not None
    assert app.name == 'app'  # Verify app module name
