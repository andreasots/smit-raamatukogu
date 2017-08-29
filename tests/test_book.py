import json
import requests
import helpers

BOOK_TITLE = "Physically Based Rendering: From Theory to Implementation, Third Edition"
BOOK_TITLE2 = BOOK_TITLE + "a"
BOOK_AUTHOR = "Matt Pharr, Wenzel Jakob, Greg Humphreys"

def test_book_lifecycle(http_session, base_url):
    # CREATE
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

    try:
        assert book["data"]["attributes"]["title"] == BOOK_TITLE
        assert book["data"]["attributes"]["author"] == BOOK_AUTHOR

        # READ
        r = http_session.get(base_url + book["links"]["self"])
        r.raise_for_status()
        assert r.json() == book

        helpers.assert_in_listing(base_url, "/api/v1/books", book["data"]["id"])

        # UPDATE
        r = http_session.patch(base_url + book["links"]["self"], data=json.dumps({
            "data": {
                "type": "book",
                "id": book["data"]["id"],
                "attributes": {
                    "title": BOOK_TITLE2,
                }
            }
        }))
        r.raise_for_status()
        book2 = r.json()
        assert book2["data"]["attributes"]["title"] == BOOK_TITLE2
    finally:
        # DELETE
        r = http_session.delete(base_url + book["links"]["self"])
        r.raise_for_status()

        r = http_session.get(base_url + book["links"]["self"])
        r.raise_for_status()
        assert r.json()["data"] is None
