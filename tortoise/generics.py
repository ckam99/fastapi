from tortoise.models import Model
from tortoise.contrib.serializer import PydanticModel, pydantic_model_creator
from typing import Dict


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


class Schema(BaseModel):
    """
    Workaround for serializing properties with pydantic until
    https://github.com/samuelcolvin/pydantic/issues/935
    is solved
    """
    @classmethod
    def get_properties(cls):
        return [prop for prop in dir(cls) if isinstance(getattr(cls, prop), property) and prop not in ("__values__", "fields")]

    def dict(
        self,
        *,
        include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> 'DictStrAny':
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )
        props = self.get_properties()
        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        # Update the attribute dict with the properties
        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})

        return attribs
