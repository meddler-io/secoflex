from typing import Optional, List
from .dbmodel import DBModelMixin
from pydantic.types import constr, Any
from ..core.jwt import create_access_token, get_file_from_token
from enum import Enum, IntEnum
from .rwmodel import RWModel
from pydantic import validator
import ipaddress
from ipaddress import ip_address
from pydantic import BaseModel, validator, HttpUrl
from pydantic import Schema
from datetime import datetime
import re
from urllib.parse import urlparse

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


class AssetSchema(DBModelMixin):
    tyoe: AssetType
    name: str = ""
    identifier: str = ""
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    active: Optional[bool] = True
    group: Optional[str]


# Host
class HostAssetSchema(RWModel, AssetSchema):
    tyoe = AssetType.HOST
    value: IpAddress
    health: HostHealthType = HostHealthType.UP
    pass


class HostAssetSchemaResponse(RWModel, AssetSchema ):
    tyoe = AssetType.HOST
    value: str = Schema(..., alias="host")
    health: HostHealthType = HostHealthType.UP
    pass

# Domain

class DomainAssetSchema(RWModel, AssetSchema ):
    tyoe = AssetType.DOMAIN
    value: str

    @validator('value')
    def must_be_domain(cls, v):

        pattern = re.compile(
           '^([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}$', re.IGNORECASE)
        if pattern.match(v):
            return v
        else:

            try:
                domain = urlparse(v)[1]

            except:
                raise ValueError("Must be a valid URL")

            if len(domain) < 1:
                raise ValueError("Must be a valid URL")
            return domain


class DomainAssetSchemaResponse(RWModel, AssetSchema ):
    tyoe: AssetType
    value: str = Schema(..., alias="domain")

    pass


# Web
class WebAssetSchema(RWModel, AssetSchema):
    tyoe = AssetType.WEB
    value: str
    url: Optional[Url] = None

    @validator('url', always=True)
    def must_be_url(cls, v, values):
        from urllib.parse import urlparse
        print("Validating url", cls, v, values["value"])
        try:
            url = urlparse(
                values["value"])
        except:
            raise ValueError("Must be a valid URL")

        return Url(scheme=url[0], netloc=url[1], path=url[2], params=url[3], query=url[4], fragment=url[5])


class WebAssetSchemaResponse(RWModel ):
    tyoe: AssetType
    name: str
    identifier: str
    value: str = Schema(..., alias="value")
    url: Optional[Url]

    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    active: bool
    group: Optional[str]
    pass



# Android
class AndroidAssetSchema(RWModel, AssetSchema):
    tyoe = AssetType.ANDROID
    value: str
    package_name: Optional[str]
    app_name: Optional[str]



class AndroidAssetSchemaResponse(RWModel ):
    tyoe: AssetType
    app_name: Optional[str]
    identifier: Optional[str]
    package_name: Optional[str]
    app_name: Optional[str]
    value: str = Schema(..., alias="file_id")
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    group: Optional[str]



# Ios
class IosAssetSchema(RWModel, AssetSchema):
    tyoe = AssetType.IOS
    value: str
    package_name: Optional[str]
    app_name: Optional[str]



class IosdAssetSchemaResponse(RWModel ):
    tyoe: AssetType
    app_name: Optional[str]
    identifier: Optional[str]
    package_name: Optional[str]
    app_name: Optional[str]
    value: str = Schema(..., alias="file_id")
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    group: Optional[str]


# REPOSITORY
class RepositoryAssetSchema(RWModel, AssetSchema):
    tyoe = AssetType.REPOSITORY
    credential_type: str
    url: str
    credentials: Any


class RepositoryAssetSchemaResponse(RWModel ):
    tyoe: AssetType
    identifier: Optional[str]
    tyoe = AssetType.REPOSITORY
    credential_type: str
    url: str
    name: str
    credentials: Any
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    group: Optional[str]


# DOCKER
class DockerAssetSchema(RWModel, AssetSchema):
    tyoe = AssetType.DOCKER
    credential_type: str
    url: str
    name: str
    credentials: Any


class DockerAssetSchemaResponse(RWModel ):
    tyoe: AssetType
    identifier: Optional[str]
    tyoe = AssetType.REPOSITORY
    credential_type: str
    url: str

    credentials: Any
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    group: Optional[str]
