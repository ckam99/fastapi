from tortoise import fields
from tortoise.models import Model


class Address(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    country = fields.CharField(max_length=100)
    region = fields.CharField(max_length=100)
    city = fields.CharField(max_length=100)
    street = fields.CharField(max_length=100)
    index = fields.CharField(max_length=100, null=True)

    class Meta:
        table = 'addresses'
