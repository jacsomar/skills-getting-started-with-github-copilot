def test_signup_successfully_adds_participant(client):
    new_email = "new-student@mergington.edu"

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": new_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert new_email in participants


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_student_across_activities(client):
    duplicate_email = "michael@mergington.edu"

    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": duplicate_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for an activity"


def test_signup_returns_422_when_email_is_missing(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422


def test_signup_then_unregister_flow(client):
    flow_email = "flow-student@mergington.edu"

    signup_response = client.post(
        "/activities/Debate%20Society/signup",
        params={"email": flow_email},
    )
    assert signup_response.status_code == 200

    after_signup = client.get("/activities").json()
    assert flow_email in after_signup["Debate Society"]["participants"]

    unregister_response = client.delete(
        "/activities/Debate%20Society/signup",
        params={"email": flow_email},
    )
    assert unregister_response.status_code == 200

    after_unregister = client.get("/activities").json()
    assert flow_email not in after_unregister["Debate Society"]["participants"]
