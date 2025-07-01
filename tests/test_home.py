# isort: off
import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the Flask app after path is adjusted
from app import app  # noqa
# isort: on


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.testing = True
    return app.test_client()


def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Fitness Club" in response.data


def test_home_page_title(client):
    """Test that the home page has the correct title."""
    response = client.get('/')
    assert b"Fitness Club Membership System" in response.data


def test_home_page_contains_emoji(client):
    """Test that the home page contains the fitness emoji."""
    response = client.get('/')
    assert "🏋️‍♂️" in response.data.decode('utf-8')
