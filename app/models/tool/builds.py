from app.models.dbmodel import DBModelMixin
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


class BuildMessageSpec(DBModelMixin):
    entrypoint: List[str] = list()
    cmd: List[str] = list()
    args: List[str] = list()
    substitute_var: bool
    variables: Dict[str, str] = dict()
    environ: Dict[str, str] = dict()
    config: Optional[BuildConfig]
    success_endpoint: str
    failure_endpoint: str
    dependencies: List[Dict] = []

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
