

from typing import Union
from pydantic.fields import Schema
from pydantic.main import BaseModel
from app.models.tool.build.common import AuthType, AuthNone, AuthCredentials, AuthToken, AuthSsh, BaseBuildModel, BuildType


class DockerPrivateAuthNone(BaseModel):
    mode: AuthType = Schema(AuthType.NONE, const=True)
    auth: AuthNone

class DockerPrivateAuthCredentials(BaseModel):
    mode: AuthType = Schema(AuthType.CREDENTIALS, const=True)
    auth: AuthCredentials



class DockerPrivateBuildConfig(BaseModel):
    image_name: str
    image_tag: str
    registry_url: str


class DockerPrivateBuild(BaseModel):
    type: BuildType = Schema(BuildType.REGISTRY_PRIVATE, const=True)
    config: DockerPrivateBuildConfig


class DockerPrivateUrlInBase(BaseBuildModel):
    auth: Union[DockerPrivateAuthNone, DockerPrivateAuthCredentials ]
    build: DockerPrivateBuild
    refrence_id: str



class DockerPrivateUrlInDB(DockerPrivateUrlInBase):
    pass


class DockerPrivaterlInReq(DockerPrivateUrlInBase):
    pass


class DockerPrivateInResp(DockerPrivateUrlInBase):
    pass
