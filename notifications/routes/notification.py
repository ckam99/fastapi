from fastapi import APIRouter, Depends, BackgroundTasks, Response
from repositories.notification import NotificationRepository
from schemas.notification import NotificationSchema
from typing import List


router = APIRouter(prefix='/notifications', tags=['Notifications'])


@router.get('/', response_model=List[NotificationSchema])
async def get_notifications(repository: NotificationRepository = Depends()):
    return await repository.fetch_all()


@router.get('/{notification_id}', response_model=NotificationSchema)
async def get_notification(notification_id: int, repository: NotificationRepository = Depends()):
    return await repository.fetch_one(notification_id)


@router.delete('/{notification_id}', response_model=None)
async def delete_notification(notification_id: int, background_tasks: BackgroundTasks,
                              repository: NotificationRepository = Depends()):
    await repository.remove(notification_id)
    return Response(status_code=204)
