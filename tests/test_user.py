import json
import requests
import helpers

USER_NAME = "Andreas Ots"
USER_NAME2 = USER_NAME + "a"

def test_user_lifecycle(http_session, base_url):
    # CREATE
    r = http_session.post(base_url + "/api/v1/users", data=json.dumps({
        "data": {
            "type": "user",
            "attributes": {
                "name": USER_NAME,
            },
        },
    }))

    r.raise_for_status()
    user = r.json()

    try:
        assert user["data"]["attributes"]["name"] == USER_NAME

        # READ
        r = http_session.get(base_url + user["links"]["self"])
        r.raise_for_status()
        assert r.json() == user

        helpers.assert_in_listing(base_url, "/api/v1/users", user["data"]["id"])

        # UPDATE
        r = http_session.patch(base_url + user["links"]["self"], data=json.dumps({
            "data": {
                "type": "user",
                "id": user["data"]["id"],
                "attributes": {
                    "name": USER_NAME2,
                }
            }
        }))
        r.raise_for_status()
        user2 = r.json()
        assert user2["data"]["attributes"]["name"] == USER_NAME2
    finally:
        # DELETE
        r = http_session.delete(base_url + user["links"]["self"])
        r.raise_for_status()

        r = http_session.get(base_url + user["links"]["self"])
        r.raise_for_status()
        assert r.json()["data"] is None
