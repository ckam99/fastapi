from . import testclient
import json
from apps.base import services


def test_register_user(testclient, monkeypatch):
    request_payload = {
        "name": "string",
        "username": "string",
        "email": "user@example.com",
        "password": "string"
    }
    response_payload = {
        "name": "string",
        "username": "string00",
        "email": "user00@example.com",
        "id": 20,
        "avatar": ''
    }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(services, "post", mock_post)

    response = testclient.post(
        "/auth/register/", data=json.dumps(request_payload),)

    assert response.status_code == 201
    assert response.json() == response_payload
