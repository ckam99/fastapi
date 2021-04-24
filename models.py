from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(50, null=True)
    username = fields.CharField(50, unique=True)
    email = fields.CharField(255, unique=True)
    password = fields.CharField(255, null=True)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return True

    def set_password(self, password):
        pass
