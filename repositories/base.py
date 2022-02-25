from abc import ABC, abstractmethod, abstractproperty
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


class BaseRepository(ABC):

    @abstractproperty
    def model(self):
        pass

    @property
    def serializer(self):
        return pydantic_model_creator(self.model)


class Repository(BaseRepository):

    @abstractmethod
    async def getAll(limit: int = 100, skip: int = 0) -> list[BaseModel]:
        pass

    @abstractmethod
    async def findOne(self, *args, **kwargs):
        pass

    @abstractmethod
    async def create(*args, **kwargs) -> BaseModel:
        pass

    @abstractmethod
    async def update(id: int, *args, **kwargs) -> BaseModel:
        pass

    @abstractmethod
    async def remove(id: int):
        pass
