from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_adds_participant_to_activity():
    activity_name = "Chess Club"
    participant_email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup?email={participant_email}"
    )

    assert response.status_code == 200
    assert participant_email in activities[activity_name]["participants"]

    activities[activity_name]["participants"].remove(participant_email)


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    participant_email = activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/participants/{participant_email}"
    )

    assert response.status_code == 200
    assert participant_email not in activities[activity_name]["participants"]

    activities[activity_name]["participants"].append(participant_email)
