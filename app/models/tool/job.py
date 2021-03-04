from app.models.dbmodel import DBModelMixin, ObjectId
from app.models.tool.integrated.docker_build import DockerImageSpec
from app.models.tool.toobuilder import ToolInResp
from pydantic.fields import Schema
from .builds import BuildMessageSpec
from typing import Optional, List, Dict
from fastapi.exceptions import HTTPException
from pydantic import validator
from pydantic.networks import HttpUrl
from pydantic.types import Any
from enum import Enum
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from ..mongo_id import ObjectIdInReq, ObjectIdInRes


class ExecutionStatus(str, Enum):
    ENQUEUED = 'ENQUEUED'
    INITIATED = 'INITIATED'
    COMPLETED = 'COMPLETED'
    TIMEOUT = 'TIMEOUT'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    UNKNOWN = 'UNKNOWN'


class JobRequestModel(BaseModel):
    job_config: BuildMessageSpec


class JobResponseModel(BaseModel):
    job_config: Any


class JobInRequest(BaseModel):
    request: JobRequestModel
    refrence_id: ObjectIdInReq = Schema(None, alias="refrence_id")


class JobInDb(DBModelMixin):
    refrence_id: ObjectId
    response: Optional[Any]
    exec_status: ExecutionStatus = ExecutionStatus.ENQUEUED
    request: JobRequestModel
    response: Optional[Any]


class JobInResponse(JobInDb):
    refrence_id: ObjectIdInRes = Schema(None, alias="refrence_id")


class JobUpdateModel(BaseModel):
    response: Any
    exec_status: ExecutionStatus = ExecutionStatus.COMPLETED
