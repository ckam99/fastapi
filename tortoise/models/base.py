from tortoise import fields, models


class User(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    lastname = fields.CharField(max_length=20)
    firstname = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def full_name(self) -> str:
        return f"{self.firstname or ''} {self.lastname or ''}".strip()

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password"]


class Post(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    body = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField(
        'models.User', related_name='posts', on_delete=fields.CASCADE)
