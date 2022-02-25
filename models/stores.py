from tortoise import fields
from tortoise.models import Model


class Store(Model):

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100)
    contact = fields.CharField(max_length=100, null=True)
    address = fields.CharField(max_length=100, null=True)
    website = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    owner = fields.ForeignKeyField(
        'models.User', related_name='store', on_delete=fields.CASCADE, null=True)

    class Meta:
        table = 'stores'

    def __str__(self) -> str:
        return self.name
