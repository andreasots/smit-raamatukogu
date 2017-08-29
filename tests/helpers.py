import requests

def assert_in_listing(base_url, start_url, id):
    url = base_url + start_url
    while url is not None:
        r = requests.get(url)
        r.raise_for_status()
        page = r.json()
        for item in page["data"]:
            if item["id"] == id:
                return
        url = base_url + page["links"]["next"]
    raise Exception("Item %d was not found in the listing" % id)
