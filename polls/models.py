from tortoise.models import Model
from tortoise import fields
from tortoise import models, fields


class Post(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=180)
    body = fields.TextField()
    picture = fields.CharField(max_length=256, null=True)
    author = fields.ForeignKeyField(
        'models.User', related_name='user', on_delete='CASCADE')

    def __str__(self):
        return self.title


class Tournament(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    # References to other models are defined in format
    # "{app_name}.{model_name}" - where {app_name} is defined in tortoise config
    tournament = fields.ForeignKeyField(
        'models.Tournament', related_name='events')
    participants = fields.ManyToManyField(
        'models.Team', related_name='events', through='event_team')

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name
