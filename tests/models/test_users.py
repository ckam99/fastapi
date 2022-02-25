import pytest
from models.users import User
from datetime import datetime

data = {
    'lastname': 'John',
    'firstname': 'Doe',
    'username': 'jdoe',
    'is_actif': False,
    'phone': '+79898713579',
    'email': 'johndoe@example.com',
    'password': '9000565',
}


@pytest.mark.asyncio
async def test_create_user():
    await User.all().delete()
    user = await User.create(**data)
    assert user.email == data['email']
    assert await User.filter(email=user.email).count() == 1


@pytest.mark.asyncio
async def test_update_user():
    user = await User.filter(email=data['email']).first()
    assert user is not None
    user.email_confirmed_at = datetime.now()
    user.is_actif = True
    update_data = {'email_confirmed_at': datetime.now(), 'is_actif': True}
    await user.update_from_dict(update_data)
    assert user.is_actif != data['is_actif']
    assert user.email_confirmed_at is not None


@pytest.mark.asyncio
async def test_remove_user():
    await User.filter(email=data['email']).delete()
    assert await User.filter(email=data['email']).count() == 0
