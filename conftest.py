import pytest
import requests

def pytest_addoption(parser):
    parser.addoption("--base-url", default="http://localhost:5000",
                     help="Base URL of the API")

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture(scope="session")
def http_session():
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/vnd.api+json",
    })

    yield session

    session.close()
