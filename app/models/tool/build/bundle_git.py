

from typing import Union
from pydantic.fields import Schema
from pydantic.main import BaseModel
from app.models.tool.build.common import AuthType, AuthNone, AuthCredentials, AuthToken, AuthSsh, BuildType


class GitAuthNone(BaseModel):
    mode: AuthType = Schema(AuthType.NONE, const=True)
    auth: AuthNone

class GitAuthCredentials(BaseModel):
    mode: AuthType = Schema(AuthType.CREDENTIALS, const=True)
    auth: AuthCredentials


class GitAuthSsh(BaseModel):
    mode: AuthType = Schema(AuthType.SSH, const=True)
    auth: AuthSsh

class GitAuthToken(BaseModel):
    mode: AuthType = Schema(AuthType.AUTHTOKEN, const=True)
    auth: AuthToken



class GitBuildConfig(BaseModel):
    repository: str
    repository_url: str


class GitBuild(BaseModel):
    type: BuildType = Schema(BuildType.BUNDLE_GIT, const=True)
    config: GitBuildConfig


class GitUrlInBase(BaseModel):
    auth: Union[GitAuthNone, GitAuthCredentials, GitAuthSsh, GitAuthToken ]
    build: GitBuild


class GitUrlInDB(GitUrlInBase):
    pass


class GitrlInReq(GitUrlInBase):
    pass


class GitInResp(GitUrlInBase):
    pass
