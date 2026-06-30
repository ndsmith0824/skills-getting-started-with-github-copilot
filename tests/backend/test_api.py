import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def restore_activities_state():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_state))


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_available_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12


def test_signup_returns_not_found_for_unknown_activity(client):
    response = client.post("/activities/Unknown Activity/signup?email=test@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    existing_email = activities["Chess Club"]["participants"][0]

    response = client.post(f"/activities/Chess Club/signup?email={existing_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_returns_not_found_for_missing_participant(client):
    response = client.delete("/activities/Chess Club/participants/newstudent@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
