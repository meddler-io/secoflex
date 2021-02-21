

from app.models.dbmodel import ObjectId
from typing import Union
from pydantic.fields import Schema
from pydantic.main import BaseModel
from app.models.tool.build.common import AuthType, AuthNone, AuthCredentials, AuthToken, AuthSsh, BaseBuildModel, BaseBuildModelInResponse, BuildType


class BundleAuthNone(BaseModel):
    mode: AuthType = Schema(AuthType.NONE, const=True)
    auth: AuthNone


class BundleBuildConfig(BaseModel):
    type: str
    url: str
    bucket: str
    filename: str
    identifier: str
    version: str

    def get_object_path(_):
        return "http://path.to.storage"


class BundleBuild(BaseModel):
    type: BuildType = Schema(BuildType.BUNDLE_UPLOAD, const=True)
    config: BundleBuildConfig


class BundleUploadInBase(BaseBuildModelInResponse):
    auth: Union[BundleAuthNone]
    build: BundleBuild




class BundleUploadInDB(BundleUploadInBase):
    pass


class BundleUploadInReq(BundleUploadInBase):
    pass


class BundleGitInResp(BundleUploadInDB):
    pass
