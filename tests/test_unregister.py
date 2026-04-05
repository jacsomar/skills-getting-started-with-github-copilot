def test_unregister_successfully_removes_participant(client):
    registered_email = "daniel@mergington.edu"

    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": registered_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {registered_email} from Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert registered_email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_member(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_returns_422_when_email_is_missing(client):
    response = client.delete("/activities/Chess%20Club/signup")

    assert response.status_code == 422
