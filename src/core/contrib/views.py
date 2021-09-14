from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from tortoise.query_utils import Q
from fastapi import HTTPException


class BaseView():
    model: Model
    pydantic: PydanticModel = None

    def __init__(self):
        if(self.pydantic is None):
            self.pydantic = pydantic_model_creator(self.model)

    async def list(self):
        return await self.pydantic.from_queryset(self.model.all())

    async def find(self,  *args: None, **kwargs: None):
        return await self.pydantic.from_queryset_single(self.model.get(*args, **kwargs))

    async def get(self,  *args: None, **kwargs: None):
        return await self.pydantic.from_queryset(self.model.get(*args, **kwargs))

    async def create(self, schema: Dict):
        data = await self.model.create(schema)
        return self.pydantic.from_orm(data)

    async def update(self, id: int, schema: Model):
        await self.model.filter(id=id).update(**schema.dict(exclude_unset=True))
        return await self.pydantic.from_queryset_single(self.model.get(id=id))

    async def delete(self, id: int):
        return await self.model.filter(id=id).delete()


class BaseModelView():
    model: Model
    serialiser_model: PydanticModel = None

    def __init__(self):
        if(self.pydantic is None):
            self.pydantic = pydantic_model_creator(self.model)

    async def create(self, schema, *args, **kwargs):
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        return await self.serialiser_model.from_tortoise_orm(obj)

    async def update(self, schema, **kwargs):
        await self.model.filter(**kwargs).update(**schema.dict(exclude_unset=True))
        return await self.serialiser_model.from_queryset_single(self.model.get(**kwargs))

    async def delete(self, **kwargs):
        obj = await self.model.filter(**kwargs).delete()
        if not obj:
            raise HTTPException(
                status_code=404, detail='Object does not exist')

    async def all(self):
        return await self.serialiser_model.from_queryset(self.model.all())

    async def filter(self, **kwargs):
        return await self.serialiser_model.from_queryset(self.model.filter(**kwargs))

    async def get(self, **kwargs):
        return await self.serialiser_model.from_queryset_single(self.model.get(**kwargs))

    async def get_obj(self, **kwargs):
        return await self.model.get_or_none(**kwargs)
