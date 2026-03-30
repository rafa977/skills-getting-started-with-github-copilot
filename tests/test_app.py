import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    # Arrange: Test client is set up above
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Cleanup: Remove the test email to avoid side effects
    activities[activity]["participants"].remove(email)

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_root_redirect():
    # Arrange: Test client is set up above
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307
    # Should redirect to /static/index.html
    if response.is_redirect:
        assert response.headers["location"].endswith("/static/index.html")
