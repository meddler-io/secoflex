

from app.models.mongo_id import ObjectId
from typing import Union
from pydantic.fields import Schema
from pydantic.main import BaseModel
from app.models.tool.build.common import AuthType, AuthNone, AuthCredentials, AuthToken, AuthSsh, BaseBuildModel, BuildType



class DockerPublicAuthNone(BaseModel):
    mode: AuthType = Schema(AuthType.NONE, const=True)
    auth: AuthNone

class DockerPublicAuthCredentials(BaseModel):
    mode: AuthType = Schema(AuthType.CREDENTIALS, const=True)
    auth: AuthCredentials




class DockerPublicBuildConfig(BaseModel):
    image_name: str
    image_tag: str


class DockerPublicBuild(BaseModel):
    type: BuildType = Schema(BuildType.REGISTRY_PUBLIC, const=True)
    config: DockerPublicBuildConfig


class DockerPublicUrlInBase(BaseBuildModel):
    auth: Union[DockerPublicAuthNone, DockerPublicAuthCredentials ]
    build: DockerPublicBuild
    refrence_id: str



class DockerPublicUrlInDB(DockerPublicUrlInBase):
    pass


class DockerPublicrlInReq(DockerPublicUrlInBase):
    pass


class DockerPublicInResp(DockerPublicUrlInBase):
    pass
