from . import testclient


def test_ping(testclient):
    response = testclient.get("/hello")
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello everybody!'}
