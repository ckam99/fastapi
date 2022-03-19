from tortoise import models, fields


class Message(models.Model):
    id = fields.BigIntField(pk=True)
    message = fields.TextField()

    def __str__(self) -> str:
        return self.message
