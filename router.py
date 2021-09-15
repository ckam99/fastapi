from fastapi import APIRouter, status, HTTPException
from services import TournamentService, EventService, TeamService
from exceptions import ModelNotFoundException
from schemas import Tournament, TournamentIn, Event, EventIn, TeamIn, Team
from typing import List


router = APIRouter()


''' Tournament '''


@router.get('/tournaments', response_model=List[Tournament], tags=['Tournaments'])
async def get_tournaments(offset: int = 0, limit: int = 100):
    return await TournamentService.all(offset=offset, limit=limit)


@router.post('/tournaments', response_model=Tournament, status_code=status.HTTP_201_CREATED, tags=['Tournaments'])
async def create_tournament(payload: TournamentIn):
    try:
        return await TournamentService.create(payload.dict())
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.get('/tournaments/{tournament_id}', response_model=Tournament, tags=['Tournaments'])
async def get_tournament(tournament_id: int):
    try:
        return await TournamentService.find(tournament_id)
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.put('/tournaments/{tournament_id}', response_model=Tournament, status_code=status.HTTP_202_ACCEPTED, tags=['Tournaments'])
async def update_tournament(tournament_id: int, payload: TournamentIn):
    try:
        return await TournamentService.update(tournament_id, payload.dict())
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.delete('/tournaments/{tournament_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Tournaments'])
async def remove_tournament(tournament_id: int):
    try:
        await TournamentService.remove(tournament_id)
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


''' Teams '''


@router.get('/teams', response_model=List[Team], tags=['Teams'])
async def get_teams(offset: int = 0, limit: int = 100):
    return await TeamService.get_teams(offset=offset, limit=limit)


@router.post('/teams', response_model=Team, status_code=status.HTTP_201_CREATED, tags=['Teams'])
async def create_team(payload: TeamIn):
    try:
        return await TeamService.create_team(payload.dict())
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.get('/teams/{team_id}', response_model=Team, tags=['Teams'])
async def get_team(team_id: int):
    try:
        return await TeamService.find_team(team_id)
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.put('/teams/{team_id}', response_model=Team, status_code=status.HTTP_202_ACCEPTED, tags=['Teams'])
async def update_team(team_id: int, payload: TeamIn):
    try:
        return await TeamService.update_team(team_id, payload.dict())
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.delete('/teams/{team_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Teams'])
async def remove_team(team_id: int):
    try:
        await TeamService.remove_team(team_id)
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


''' Events '''


@router.get('/events', response_model=List[Event], tags=['Events'])
async def get_events(offset: int = 0, limit: int = 100):
    return await EventService.get_events(offset=offset, limit=limit)


@router.post('/events', response_model=Event, status_code=status.HTTP_201_CREATED, tags=['Events'])
async def create_event(payload: EventIn):
    try:
        return await EventService.create_event(payload)
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.get('/events/{event_id}', response_model=Event, tags=['Events'])
async def get_event(event_id: int):
    try:
        return await EventService.find_event(event_id)
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.put('/events/{event_id}', response_model=Event, status_code=status.HTTP_202_ACCEPTED, tags=['Events'])
async def update_event(event_id: int, payload: EventIn):
    try:
        return await EventService.update_event(event_id, payload.dict())
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )


@router.delete('/events/{event_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Events'])
async def remove_event(event_id: int):
    try:
        await EventService.remove_event(event_id)
    except ModelNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.message
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some error occured'
        )
