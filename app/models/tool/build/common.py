# from app.models.mongo_id import ObjectId
from app.models.tool.executor import BuildExecutorInResponse
from app.models.tool.tool import ToolInResp
from app.models.mongo_id import ObjectIdInReq
from app.models.tool.builds import BuildMessageSpec
from app.models.dbmodel import DBModelMixin, ObjectId
from typing import Optional, List, Dict

from fastapi.exceptions import HTTPException
from google.auth.environment_vars import CREDENTIALS
from pydantic import Schema, validator
from pydantic.networks import HttpUrl
from pydantic.types import Any
from enum import Enum
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Union


#
# #
class AuthType(str, Enum):
    NONE = 'none'  # Will focus on this only for now
    SSH = 'ssh'
    AUTHTOKEN = 'token'
    CREDENTIALS = 'credentials'


class BaseAuth(BaseModel):
    pass


class AuthNone(BaseAuth):
    pass


class AuthCredentials(BaseAuth):
    username: str
    password: str


class AuthToken(BaseAuth):
    auth_token: str


class AuthSsh(BaseAuth):
    ssh_key: str


class AuthModel():
    auth_mode: AuthType
    auth: Union[AuthNone, AuthCredentials, AuthToken, AuthSsh]


#

class BuildType(str, Enum):
    REGISTRY_PUBLIC = 'registry_public'  # Will focus on this only for now
    REGISTRY_PRIVATE = 'registry_private'
    BUNDLE_GIT = 'bundle_git'
    BUNDLE_URL = 'bundle_url'
    BUNDLE_UPLOAD = 'bundle_upload'
    DOCKERFILE = 'dockerfile'


class BaseAuthModel(BaseModel):
    mode: AuthType
    auth: Any


class BaseBuildConfigModel(BaseModel):
    type: BuildType
    config: Any


class BuildMetaData(BaseModel):
    tags: List[str]


class BaseBuildModel(DBModelMixin):
    auth: BaseAuthModel
    build: BaseBuildConfigModel
    refrence_id: ObjectId = Schema(None, alias="refrence_id")
    build_config: Optional[BuildMessageSpec]

    # Meta
    meta: Optional[BuildMetaData]


class BaseBuildModelInResponse(BaseBuildModel):
    pass


class BaseBuildModelInRequest(BaseBuildModel):
    pass


class BaseBuildWithToolModelInResponse(BaseBuildModel):
    tool: ToolInResp
    executors: Optional[List[BuildExecutorInResponse]]
