from typing import List, Optional
from enum import Enum
from ipaddress import ip_address
from pydantic import BaseModel, Schema, Field


class IpAddress(BaseModel):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            ip_address(v)
        except:
            raise TypeError('Invalid IPAddress', v)
        return str(v)


# Remains
class BaseAssetInDB(BaseModel):
    pass


class BaseAssetInRequest(BaseModel):
    pass


class BaseAssetInResponse(BaseModel):
    pass


class Url(BaseModel):
    scheme: str
    netloc: str
    path: str
    params: str
    query: str
    fragment: str


class HostHealthType(str, Enum):
    UP = 'up'
    DOWN = 'down'
    UNKNOWN = 'unknown'


class AssetType(str, Enum):
    HOST = 'host'
    DOMAIN = 'domain'
    ANDROID = 'android'
    IOS = 'ios'
    WEB = 'web'
    REPOSITORY = 'repository'
    DOCKER = 'docker'


class ToolSchemaValidator(BaseModel):
    version: int


class ToolYamlSchemaValidator(BaseModel):
    version: int
    tools: List[ToolSchemaValidator] 


