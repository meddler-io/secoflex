


from app.models.dbmodel import ObjectId
from typing import Union
from pydantic.fields import Schema
from pydantic.main import BaseModel
from app.models.tool.build.common import BaseBuildModel, AuthType , AuthNone, AuthCredentials, AuthToken, AuthSsh, BaseBuildModelInResponse, BuildType


class DockerfileAuthNone(BaseModel):
    mode: AuthType = Schema(AuthType.NONE, const=True)
    auth: AuthNone


class DockerfileBuildConfig(BaseModel):
    dockerfile: str

class DockerfileBuild(BaseModel):
    type: BuildType = Schema(BuildType.DOCKERFILE, const=True)
    config: DockerfileBuildConfig


class DockerfileUrlInBase(BaseBuildModelInResponse):
    auth: Union[DockerfileAuthNone]
    build: DockerfileBuild
    



class DockerfileUrlInDB(DockerfileUrlInBase):
    pass


class DockerfileUrlInReq(DockerfileUrlInBase):
    pass


class DockerfileGitInResp(DockerfileUrlInDB):
    pass
