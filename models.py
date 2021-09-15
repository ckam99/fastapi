from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

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


EventORM = pydantic_model_creator(Event)
