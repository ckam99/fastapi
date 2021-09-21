from passlib.hash import bcrypt
from tortoise import fields, models


class User(models.Model):
    id = fields.BigIntField(pk=True)
    lastname = fields.CharField(max_length=20)
    firstname = fields.CharField(max_length=50, null=True)
    username = fields.CharField(50, unique=True)
    email = fields.CharField(255, unique=True)
    phone = fields.CharField(25, null=True)
    password = fields.CharField(255, null=True)
    avatar = fields.CharField(255, null=True)
    email_confirmed_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_actif = fields.BooleanField(default=True)
    roles = fields.ManyToManyField(
        'models.Role', related_name='users', through='user_roles')

    class Meta:
        table = 'users'

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password"]

    def full_name(self) -> str:
        return f"{self.firstname or ''} {self.lastname or ''}".strip()

    def __str__(self):
        return self.email

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def set_password(self, password):
        self.password = bcrypt.hash(password)


class Role(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=25, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'roles'


class Attempt(models.Model):
    id = fields.BigIntField(pk=True)
    email = fields.CharField(max_length=255)
    code = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'attempts'

    def __str__(self):
        return f'{self.email}/{self.code}'


class Notification(models.Model):
    id = fields.BigIntField(pk=True)
    type = fields.CharField(max_length=255)
    read_at = fields.DatetimeField(null=True)
    data = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField(
        'models.User',  related_name='notifications', null=True, on_delete=fields.CASCADE)

    class Meta:
        table = 'notifications'
