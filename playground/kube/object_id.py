
from bson import objectid
import bson
from pydantic import BaseModel , BaseConfig
from pydantic.fields import Field


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return objectid.ObjectId(str(v))
        except Exception:
            raise ValueError("Not a valid ObjectId")


class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            objectid.ObjectId: lambda oid: str(oid),
        }

class User(MongoModel):
    id: OID = Field()
    name: str = Field()


a = User( **{
    "id": "602be8904aaf8ff92cbd608f",
    "name": "jelo"
} )

print(a)
print(a.json())


a = User( **{
    "id":  objectid.ObjectId("602be8904aaf8ff92cbd608f"),
    "name": "jelo"
} )

print(a)
print(a.json())


