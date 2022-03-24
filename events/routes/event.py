from fastapi import APIRouter, Depends, BackgroundTasks, Response
from repositories.event import EventRepository
from schemas.event import EventSchema
from typing import List


router = APIRouter(prefix='/events', tags=['Events'])


@router.get('/', response_model=List[EventSchema])
async def get_events(repository: EventRepository = Depends()):
    return await repository.fetch_all()


@router.get('/{event_id}', response_model=EventSchema)
async def get_event(event_id: int, repository: EventRepository = Depends()):
    return await repository.fetch_one(event_id)


@router.delete('/{event_id}', response_model=None)
async def delete_event(event_id: int, background_tasks: BackgroundTasks,
                       repository: EventRepository = Depends()):
    await repository.remove(event_id)
    return Response(status_code=204)
