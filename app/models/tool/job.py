from app.models.tool.executor import BuildExecutorInResponse
from app.models.dbmodel import DBModelMixin, ObjectId
from app.models.tool.integrated.docker_build import DockerImageSpec
from app.models.tool.toobuilder import ToolInResp
from pydantic.fields import Schema
from .builds import BaseBuildInResponse, BuildMessageSpec
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
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    exec_status: ExecutionStatus = ExecutionStatus.ENQUEUED
    request: JobRequestModel
    response: Optional[Any]


class JobInResponse(JobInDb):
    refrence_id: ObjectIdInRes = Schema(None, alias="refrence_id")


class JobCompositeInResponse(JobInResponse):
    # tool_id: ObjectIdInRes = Schema(None, alias="tool_id")
    tool: Optional[ ToolInResp ]


    pass
    # job: JobInResponse
    # exec: BuildExecutorInResponse
    # build: BaseBuildInResponse


class JobUpdateModel(BaseModel):
    response: Any
    exec_status: ExecutionStatus = ExecutionStatus.COMPLETED


class JobProgressResponse(BaseModel):
    exec_status: ExecutionStatus = ExecutionStatus.COMPLETED
    poll_after: int = 1000  # Milliseconds
    poll_again: Optional[bool] = True

    @validator('poll_again', always=True)
    def build_optional_fields(cls, v, values):
        cls.poll_after = 1000
        exec_status:  ExecutionStatus = values["exec_status"]

        if exec_status == ExecutionStatus.ENQUEUED:
            cls.poll_again = True
            pass
        elif exec_status == ExecutionStatus.INITIATED:
            cls.poll_again = True

        elif exec_status == ExecutionStatus.COMPLETED:
            cls.poll_again = False

        elif exec_status == ExecutionStatus.TIMEOUT:
            cls.poll_again = False

        elif exec_status == ExecutionStatus.SUCCESS:
            cls.poll_again = False

        elif exec_status == ExecutionStatus.FAILURE:
            cls.poll_again = False

        elif exec_status == ExecutionStatus.UNKNOWN:
            cls.poll_again = True
        else:
            cls.poll_again = True

        return cls.poll_again
