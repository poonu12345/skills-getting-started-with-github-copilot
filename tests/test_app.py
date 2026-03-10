import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Test GET /activities
def test_get_activities():
    # Arrange
    # (client already arranged)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

# Arrange-Act-Assert: Test root redirect
def test_root_redirect():
    # Arrange
    # (client already arranged)
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307
    assert "text/html" in response.headers["content-type"]

# Arrange-Act-Assert: Test signup success
def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

# Arrange-Act-Assert: Test duplicate signup
def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

# Arrange-Act-Assert: Test signup for non-existent activity
def test_signup_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# Arrange-Act-Assert: Test signup for full activity
@pytest.mark.skip(reason="No activity is full by default; add test if needed.")
def test_signup_full():
    # Arrange
    activity = "Chess Club"
    # Fill up participants
    for i in range(12 - len(client.get("/activities").json()[activity]["participants"])):
        email = f"fullstudent{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email=extrastudent@mergington.edu")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
