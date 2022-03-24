from tortoise import models, fields
from enum import Enum


class NotificationStatus(str, Enum):
    NONE = 'none'
    ERROR = 'error'
    SENT = 'sent'
    PENDING = 'pending'


class Notification(models.Model):
    id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=60)
    description = fields.TextField(null=True, blank=True)
    source = fields.CharField(max_length=60, null=True)
    body = fields.JSONField(null=True)
    status = fields.CharEnumField(
        enum_type=NotificationStatus, default=NotificationStatus.NONE)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
    user_id = fields.BigIntField(null=True)

    def __str__(self) -> str:
        return self.message

    class Meta:
        table = 'notifications'
