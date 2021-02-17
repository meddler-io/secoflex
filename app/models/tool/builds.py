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
from ..mongo_id import ObjectId
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


class ProcessConstants(BaseModel):
    input_api: Optional[str]
    input_api_token: Optional[str]
    output_api: Optional[str]
    file_upload_api: Optional[str]


class ReservedConstants(BaseModel):
    message_queue_topic: Optional[str]


class SystemConstants(BaseModel):
    base_path: Optional[str]
    input_dir: Optional[str]
    output_dir: Optional[str]
    results_json: Optional[str]
    results_schema: Optional[str]
    log_to_file: Optional[str]
    stdout_file: Optional[str]
    stderr_file: Optional[str]
    enable_logging: Optional[str]
    max_output_filesize: Optional[str]
    sample_inputfile: Optional[str]
    sample_outputfile: Optional[str]


class BuildConfig(BaseModel):
    # process: Optional[ProcessConstants]
    # reserved: Optional[ReservedConstants]
    # system: Optional[SystemConstants]
    process: Dict[str, Any] = dict()
    reserved: Dict[str, Any] = dict()
    system: Dict[str, Any] = dict()


class BuildMessageSpec(BaseModel):
    id: str
    entrypoint: List[str] = list()
    cmd: str
    args: List[str] = list()
    substitute_var: bool
    variables: Dict[str, str] = dict()
    config: Optional[BuildConfig]
    success_endpoint: str
    failure_endpoint: str

    # success_endpoint = "http://localhost:8000/api/v2/success"
    # failure_endpoint = "http://localhost:8000/api/v2/failure"


class BaseBuildInResponse(BaseModel):
    refrence_id: str
    name: str = ""
    description: str = ""
    version: str = ""
    tags: List[str] = list()
    type: BuildType
    metadata: Dict = dict()
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    build_config: Optional[BuildMessageSpec]


class BaseBuildType(BaseModel):
    refrence_id: str
    name: str = ""
    description: str = ""
    version: str = ""
    tags: List[str] = list()
    type: BuildType
    metadata: Dict = dict()
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    build_config: Optional[BuildMessageSpec]


# Registry
# Registry Public


class RegistryAuthTypes(str, Enum):
    NONE = "none"
    CREDENTIALS = "credentials"
    TOKEN = "token"


class RegistryPublicInBase(BaseBuildType):
    pass


class RegistryPublicInDB(RegistryPublicInBase):
    type: BuildType = BuildType.REGISTRY_PUBLIC
    authentication: RegistryAuthTypes
    image_name: str
    image_tag: str
    username: Optional[str]
    password: Optional[str]
    auth_token: Optional[str]


class RegistryPublicInReq(RegistryPublicInBase):
    image_name: str
    image_tag: str
    username: Optional[str]
    password: Optional[str]
    auth_token: Optional[str]
    authentication: RegistryAuthTypes

    @ validator('authentication')
    def prevent_none(cls, v, values):
        if v == RegistryAuthTypes.NONE:
            values["username"] = None
            values["password"] = None
            values["auth_token"] = None
            pass
        elif v == RegistryAuthTypes.CREDENTIALS:
            values["auth_token"] = None
            if values["username"] == None or values["password"] == None:
                raise HTTPException(401, "Auth data invalid")

        elif v == RegistryAuthTypes.TOKEN:
            values["username"] = None
            values["password"] = None
            if values["auth_token"] == None:
                raise HTTPException(401, "Auth data invalid")
            pass
        else:
            raise HTTPException(401, "Auth data invalid")
        # assert v is not None, 'size may not be None'
        return v


class RegistryPublicInResp(RegistryPublicInDB):
    pass


# Registry Private
class RegistryPrivateInBase(BaseBuildType):
    pass


class RegistryPrivateInDB(RegistryPublicInBase):
    type: BuildType = BuildType.REGISTRY_PRIVATE
    registry_url: HttpUrl
    authentication: RegistryAuthTypes
    image_name: str
    image_tag: str
    username: str
    password: str
    auth_token: str


class RegistryPrivateInReq(RegistryPublicInBase):
    registry_url: str
    authentication: RegistryAuthTypes
    image_name: str
    image_tag: str
    username: str
    password: str
    auth_token: str


class RegistryPrivateInResp(RegistryPrivateInDB):
    pass


# Bubdke

class BundleType(str, Enum):
    ZIP = "zip"
    TAR = "tar"


class RepositoryType(str, Enum):
    GITHUB = "github"
    BITBUCKET = "bitbucket"
    GITLAB = "gitlab"


class RepositoryAuthType(str, Enum):
    NONE = "none"
    CREDENTIALS = "credentials"
    TOKEN = "token"
    SSH = "ssh"


# Bundle GIT

class BundleGitInBase(BaseBuildType):
    repository: RepositoryType
    repository_url: str
    authentication: RepositoryAuthType
    username: str
    password: str
    token: str
    ssh: str


class BundleGitInDB(BundleGitInBase):
    pass


class BundleGitInReq(BundleGitInBase):
    pass


class BundleGitInResp(BundleGitInDB):
    pass


# Bundle URL


class BundleAuthNone(BaseModel):
    mode: AuthType = Schema(AuthType.NONE, const=True)
    auth: AuthNone


class BundleAuthCredentials(BaseModel):
    mode: AuthType = Schema(AuthType.CREDENTIALS, const=True)
    auth: AuthCredentials


class BundleBuildConfig(BaseModel):
    type: str
    url: str


class BundleBuild(BaseModel):
    type: BuildType
    config: BundleBuildConfig


class BundleUrlInBase(BaseModel):
    auth: Union[BundleAuthNone, BundleAuthCredentials]
    build: BundleBuild


class BundleUrlInDB(BundleUrlInBase):
    pass


class BundleUrlInReq(BundleUrlInBase):
    pass


class BundleGitInResp(BundleUrlInDB):
    pass


# Bundle Upload

class BundleUploadInBase(BaseModel):
    type: BundleType
    url: str


class BundleUploadInDB(BundleUploadInBase):
    pass


class BundleUploadInReq(BundleUploadInBase):
    pass


class BundleUploadInResp(BundleUploadInDB):
    pass


class Test(BaseModel):
    auth: AuthType
    build: BuildType
