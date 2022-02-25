import pytest
from httpx import AsyncClient
from main import app
from models.users import User


@pytest.mark.asyncio
async def test_create_user():
    name, age = ["sam", 99]

    assert await User.filter(email=name).count() == 0

    # data = {"username": name, "age": age}
    # async with AsyncClient(app=app, base_url="http://test") as ac:
    #     response = await ac.post("/testpost", json=data)
    #     assert response.json() == dict(data, id=1)
    #     assert response.status_code == 200

    #     response = await ac.get("/users")
    #     assert response.status_code == 200
    #     assert response.json() == [dict(data, id=1)]

    # assert await User.filter(username=name).count() == 1
