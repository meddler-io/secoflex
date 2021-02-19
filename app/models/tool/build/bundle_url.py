

from app.models.mongo_id import ObjectId
from typing import Union
from pydantic.fields import Schema
from pydantic.main import BaseModel
from app.models.tool.build.common import AuthType, AuthNone, AuthCredentials, AuthToken, AuthSsh, BaseBuildModel, BuildType


class BundleAuthNone(BaseModel):
    mode: AuthType = Schema(AuthType.NONE, const=True)
    auth: AuthNone


class BundleBuildConfig(BaseModel):
    type: str
    url: str


class BundleBuild(BaseModel):
    type: BuildType = Schema(BuildType.BUNDLE_URL, const=True)
    config: BundleBuildConfig


class BundleUrlInBase(BaseBuildModel):
    auth: Union[BundleAuthNone]
    build: BundleBuild
    refrence_id: str



class BundleUrlInDB(BundleUrlInBase):
    pass


class BundleUrlInReq(BundleUrlInBase):
    pass


class BundleGitInResp(BundleUrlInDB):
    pass
