from tortoise.models import Model
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator
from typing import Dict
from fastapi.templating import Jinja2Templates
from fastapi import Request

template = Jinja2Templates(directory='resources/templates')


def render(request: Request, template_name: str, context: dict = None, ):
    context = {} if context is None else context
    context['request'] = request
    return template.TemplateResponse(template_name, context)


class APIView():
    model: Model = None
    serializer: PydanticModel = None

    def __init__(self):
        if(self.serializer is None):
            self.serializer = pydantic_model_creator(self.model)

    async def all(self):
        return await self.serializer.from_queryset(self.model.all())

    async def find(self,  *args: None, **kwargs: None):
        return await self.serializer.from_queryset_single(self.model.get(*args, **kwargs))

    async def get(self,  *args: None, **kwargs: None):
        return await self.serializer.from_queryset(self.model.get(*args, **kwargs))

    async def create(self, schema: Dict):
        data = await self.model.create(schema)
        return self.serializer.from_orm(data)

    async def update(self, id: int, schema: Model):
        await self.model.filter(id=id).update(**schema.dict(exclude_unset=True))
        return await self.serializer.from_queryset_single(self.model.get(id=id))

    async def delete(self, id: int):
        return await self.model.filter(id=id).delete()
