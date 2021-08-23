from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt


class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(50, null=True)
    username = fields.CharField(50, unique=True)
    email = fields.CharField(255, unique=True)
    phone = fields.CharField(25, null=True)
    password = fields.CharField(255, null=True)
    avatar = fields.CharField(255, null=True)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def set_password(self, password):
        self.password = bcrypt.hash(password)
