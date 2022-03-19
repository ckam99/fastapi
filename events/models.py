from tortoise import fields
from tortoise.models import Model


class Event(Model):
    id = fields.BigIntField(pk=True)
    source = fields.CharField(max_length=60, null=True)
    payload = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
