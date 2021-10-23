from blog.models import User
from datetime import datetime


def create_user(payload: dict):
    user = User()
    user.lastname = payload.get('lastname')
    user.email = payload.get('email')
    user.password = payload.get('password')
    # user.created_at = datetime.strptime(
    #     payload.get('password'), '%d/%m/%y %H:%M:%S')
    user.save()
