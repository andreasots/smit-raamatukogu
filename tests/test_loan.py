import json
import requests
import helpers

BOOK_TITLE = "Physically Based Rendering: From Theory to Implementation, Third Edition"
BOOK_AUTHOR = "Matt Pharr, Wenzel Jakob, Greg Humphreys"
USER_NAME = "Andreas Ots"

def test_loan_lifecycle(http_session, base_url):
    user = None
    book = None
    loan = None

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
        r = http_session.post(base_url + "/api/v1/books", data=json.dumps({
            "data": {
                "type": "book",
                "attributes": {
                    "title": BOOK_TITLE,
                    "author": BOOK_AUTHOR,
                },
            },
        }))
        r.raise_for_status()
        book = r.json()

        # CREATE
        r = http_session.post(base_url + "/api/v1/loans", params={"include": "book,borrower"}, data=json.dumps({
            "data": {
                "type": "loan",
                "attributes": {
                },
                "relationships": {
                    "borrower": {
                        "data": {
                            "type": "user",
                            "id": user["data"]["id"],
                        },
                    },
                    "book": {
                        "data": {
                            "type": "book",
                            "id": book["data"]["id"],
                        },
                    },
                },
            },
        }))
        r.raise_for_status()
        loan = r.json()

        assert loan["data"]["relationships"]["borrower"]["data"]["id"] == user["data"]["id"]
        assert loan["data"]["relationships"]["book"]["data"]["id"] == book["data"]["id"]

        # READ
        r = http_session.get(base_url + loan["links"]["self"], params={"include": "book,borrower"})
        r.raise_for_status()
        assert r.json() == loan

        helpers.assert_in_listing(base_url, "/api/v1/loans", loan["data"]["id"])
    finally:
        # DELETE
        if loan is not None:
            r = http_session.delete(base_url + loan["links"]["self"])
            r.raise_for_status()

            r = http_session.get(base_url + loan["links"]["self"])
            r.raise_for_status()
            assert r.json()["data"] is None
        if book is not None:
            r = http_session.delete(base_url + book["links"]["self"])
            r.raise_for_status()
        if user is not None:
            r = http_session
