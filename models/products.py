from tortoise import fields
from tortoise.models import Model


class Brand(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, db_index=True)

    class Meta:
        table = 'brands'


class Category(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, db_index=True)
    parent = fields.ForeignKeyField(
        'models.Category', on_delete=fields.SET_NULL, null=True, related_name='children')

    class Meta:
        table = 'categories'

    def __str__(self) -> str:
        return self.name


class Product(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, db_index=True)
    slug = fields.CharField(max_length=255, db_index=True, null=True)
    description = fields.TextField(null=True)
    price = fields.DecimalField(decimal_places=2, default=0, max_digits=17)
    quantity = fields.IntField(default=0)
    barcode = fields.CharField(max_length=13, db_index=True, null=True)
    vat = fields.DecimalField(decimal_places=2, default=0, max_digits=5)
    weight = fields.DecimalField(decimal_places=2, default=0, max_digits=17)
    length = fields.DecimalField(decimal_places=2, default=0, max_digits=17)
    height = fields.DecimalField(decimal_places=2, default=0, max_digits=17)
    width = fields.DecimalField(decimal_places=2, default=0, max_digits=17)

    category = fields.ForeignKeyField(
        'models.Category', null=True, on_delete=fields.SET_NULL)

    brand = fields.ForeignKeyField(
        'models.Brand', null=True, on_delete=fields.SET_NULL)

    class Meta:
        table = 'products'

    def __str__(self) -> str:
        return self.name


class Image(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255, db_index=True)
    is_main = fields.BooleanField(default=False)
    product = fields.ForeignKeyField(
        'models.Product', related_name='images', null=True, on_delete=fields.CASCADE)

    class Meta:
        table = 'images'

    def __str__(self) -> str:
        return self.name
