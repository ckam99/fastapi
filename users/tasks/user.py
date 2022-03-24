from core.kafka import Kafka
from schemas.user import UserSchema


async def user_created(msg: UserSchema):
    data = {}
    data['source'] = 'users-service'
    data['data'] = msg.dict()
    await Kafka.produce('user-created-event', data)
    print('produce user create')


async def user_updated(msg: UserSchema):
    data = {}
    data['source'] = 'users-service'
    data['data'] = msg.dict()
    await Kafka.produce('user-updated-event', data)


async def user_deleted(msg: UserSchema):
    data = {}
    data['source'] = 'users-service'
    data['data'] = msg.dict()
    await Kafka.produce('user-deleted-event', data)
