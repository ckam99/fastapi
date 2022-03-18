from fastapi import APIRouter, Depends, BackgroundTasks, Response
from repositories.message import MessageRepository
from schemas.message import Message
from typing import List
from tasks.message import message_created


router = APIRouter(prefix='/messages')


@router.get('/', response_model=List[Message])
async def get_messages(repository: MessageRepository = Depends()):
    return await repository.fetch_all()


@router.post('/', response_model=Message)
async def create_message(data: Message, background_tasks: BackgroundTasks,
                         repository: MessageRepository = Depends()):
    post = await repository.create(data)
    background_tasks.add_task(message_created, 'message_created', post.dict())
    return post


@router.get('/{message_id}', response_model=Message)
async def get_message(message_id: int, repository: MessageRepository = Depends()):
    return await repository.fetch_one(message_id)


@router.put('/{message_id}', response_model=Message)
async def update_message(message_id: int, repository: MessageRepository = Depends()):
    return await repository.up(message_id)


@router.delete('/{message_id}')
async def delete_message(message_id: int, background_tasks: BackgroundTasks,
                         repository: MessageRepository = Depends()):
    post = await repository.remove(message_id)
    background_tasks.add_task(message_created, 'message_deleted', post)
    return Response(status_code=204)
