
from models import Tournament, Event, Team, EventORM
from exceptions import ModelNotFoundException
from schemas import EventIn
from typing import List


class TeamService():

    @staticmethod
    async def get_teams(offset: int = 0, limit: int = 999):
        teams = await Team.all().offset(offset).limit(limit)
        return teams

    @staticmethod
    async def create_team(data: dict):
        team = await Team.create(**data)
        return team

    @staticmethod
    async def find_team(id: int):
        team = await Team.filter(id=id).first()
        if team is None:
            raise ModelNotFoundException(
                'Team', f'Team with {id} does not exist')
        return team

    @staticmethod
    async def update_team(id: int, data: dict):
        team = await TeamService.find(id)
        await team.update_from_dict(data)
        await team.save()
        return team

    @staticmethod
    async def remove_team(id: int):
        team = await TeamService.find(id)
        await team.delete()


class TournamentService:

    @staticmethod
    async def all(offset: int = 0, limit: int = 999):
        result = await Tournament.all().offset(offset).limit(limit)
        return result

    @staticmethod
    async def create(data: dict):
        result = await Tournament.create(**data)
        return result

    @staticmethod
    async def find(id: int):
        tournament = await Tournament.filter(id=id).first()
        if tournament is None:
            raise ModelNotFoundException(
                'Tournament', f'Tournament with {id} does not exist')
        return tournament

    @staticmethod
    async def update(id: int, data: dict):
        tournament = await TournamentService.find(id)
        await tournament.update_from_dict(data)
        await tournament.save()
        return tournament

    @staticmethod
    async def remove(id: int):
        tournament = await TournamentService.find(id)
        await tournament.delete()


class EventService():

    @staticmethod
    async def get_events(offset: int = 0, limit: int = 999) -> List[Event]:
        events = await EventORM.from_queryset(Event.all().offset(offset).limit(limit))
        return events

    @staticmethod
    async def create_event(data: EventIn) -> Event:
        event = await Event.create(name=data.name, tournament_id=data.tournament)
        participants = []
        for team_id in data.participants:
            team = await TeamService().find_team(team_id)
            participants.append(team)
        await event.participants.add(*participants)
        return event

    @staticmethod
    async def find_event(id: int) -> Event:
        event = await Event.filter(id=id).first()
        if event is None:
            raise ModelNotFoundException(
                'Event', f'Event with {id} does not exist')
        return event

    @staticmethod
    async def update_event(id: int, data: EventIn) -> Event:
        event = await EventService.find_event(id)
        event.name = data.name
        event.tournament_id = data.tournament
        await event.save()
        for team_id in data.participants:
            team = await TeamService().find_team(team_id)
            await event.participants.add(team)
        return event

    @staticmethod
    async def remove_event(id: int):
        event = await EventService.find(id)
        await event.delete()
