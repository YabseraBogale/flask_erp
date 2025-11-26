import pytest
from app import app as flask_app  
import os

@pytest.fixture()
def app():
    # 1. Update config for testing
    flask_app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  
        "SECRET_KEY":os.getenv("SECRET_KEY"),
        "CACHE_TYPE":"redis",
        "CACHE_REDIS_HOST":"localhost",
        "CACHE_REDIS_PORT":"6379",
        "CACHE_REDIS_DB":0
    })

    
    yield flask_app

   

@pytest.fixture()
def client(app):
    # This creates the "browser" you use to send requests
    return app.test_client()