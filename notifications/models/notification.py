from tortoise import models, fields
from enum import Enum


class NotificationStatus(Enum):
    NONE = 'none'
    ERROR = 'error'
    SENT = 'sent'
    PENDING = 'pending'


class User(models.Model):
    id = fields.BigIntField(pk=True)
    lastname = fields.CharField(max_length=20)
    firstname = fields.CharField(max_length=50, null=True)
    email = fields.CharField(255, unique=True)
    password = fields.CharField(255, null=True)
    email_confirmed_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
    is_actif = fields.BooleanField(default=True)

    class Meta:
        table = 'users'


class Notification(models.Model):
    id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=60)
    source = fields.CharField(max_length=60, null=True)
    body = fields.JSONField()
    status = fields.CharEnumField(
        enum_type=NotificationStatus, default=NotificationStatus.NONE)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)

    def __str__(self) -> str:
        return self.message

    class Meta:
        table = 'notifications'
