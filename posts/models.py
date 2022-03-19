from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    email = fields.CharField(max_length=60, null=True, unique=True)
    name = fields.CharField(max_length=60, null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)


class Post(Model):
    id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=60, null=True)
    body = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
    user = fields.ForeignKeyField(
        'models.User', related_name='posts', null=True)
