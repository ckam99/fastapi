from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=60)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255, null=True, blank=True)


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=60, index=True)
    body = fields.TextField()
    image = fields.CharField(max_length=255, null=True, blank=True)
    owner = fields.ForeignKeyField(
        'models.User', related_name='posts', null=True, blank=True)

    def __str__(self) -> str:
        return self.title
