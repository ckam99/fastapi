from tortoise import models, fields


class Event(models.Model):
    id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=60)
    source = fields.CharField(max_length=60)
    description = fields.TextField(null=True, blank=True)
    payload = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)

    class Meta:
        table = 'events'
