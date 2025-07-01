from app import app
import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the Flask app


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
    assert app.testing == False  # Should be False by default
