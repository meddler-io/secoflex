from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Schema, Field
from bson import ObjectId as BsonObjectId


class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)



class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Schema( None , alias="createdAt")
    updated_at: Optional[datetime] = Schema( None , alias="updatedAt")


class DBModelMixin(DateTimeModelMixin):
    # id: Optional[int]
    id: Optional[ObjectId] = Schema(None, alias="_id")
    