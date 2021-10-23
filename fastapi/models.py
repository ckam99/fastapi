from tortoise import models, fields


class User(models.Model):
    id = fields.IntField(pk=True)
    firstname = fields.CharField(max_length=60, null=True)
    lastname = fields.CharField(max_length=30, null=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(null=True)


class Post(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    body = fields.TextField(max_length=255)
    created_at = fields.DatetimeField(null=True)
    user = fields.ForeignKeyField('models.User', related_name='posts')
