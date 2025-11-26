import pytest
from app import app as flask_app  
import os

@pytest.fixture()
def app():
    # 1. Update config for testing
    flask_app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  # Disables CSRF so you don't need tokens
        "SECRET_KEY":os.getenv("SECRET_KEY") # Fixes the "Secret Key Required" error
    })

    
    yield flask_app

   

@pytest.fixture()
def client(app):
    # This creates the "browser" you use to send requests
    return app.test_client()