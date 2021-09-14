import pytest
from starlette.testclient import TestClient
from core import app

client = TestClient(app)


@pytest.fixture(scope="module")
def testclient():
    client = TestClient(app)
    yield client
