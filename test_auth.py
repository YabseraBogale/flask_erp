# test_auth.py

def test_login_successful(client):
    """Test that valid credentials result in a 200 OK."""
    
    # Send POST request
    response = client.post("/login", data={
        "employee_id": "123",
        "password": "389LDW0:pmDA6Z*"
    })

    # Assertions
    assert response.status_code == 302
    # If your view returns text/JSON, you can check that too:
    # assert b"Login successful" in response.data

