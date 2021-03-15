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
from ..mongo_id import ObjectId, ObjectIdInReq, ObjectIdInRes


class ExecutionStatus(str, Enum):
    ENQUEUED = 'ENQUEUED'
    INITIATED = 'INITIATED'
    COMPLETED = 'COMPLETED'
    TIMEOUT = 'TIMEOUT'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    UNKNOWN = 'UNKNOWN'


class BuildExecutorInBase(BuildMessageSpec):
    result: Optional[DockerImageSpec]


class BuildExecutorInRequest(BuildExecutorInBase):
    refrence_id: ObjectIdInReq = Schema(None, alias="refrence_id")
    exec_status: Optional[ExecutionStatus] = ExecutionStatus.UNKNOWN


class BuildExecutorInDb(BuildExecutorInBase):
    refrence_id: ObjectId = Schema(None, alias="refrence_id")
    exec_status: ExecutionStatus = ExecutionStatus.ENQUEUED
    result: Optional[DockerImageSpec]


class BuildExecutorInResponse(BuildExecutorInBase):
    refrence_id: ObjectId = Schema(None, alias="refrence_id")
    exec_status: Optional[ExecutionStatus] = ExecutionStatus.UNKNOWN
    tool: ToolInResp = Schema(None, alias="tool")
    result: Optional[DockerImageSpec]



class BuildExecutorCompositeInResponse(BuildExecutorInBase):
    refrence_id: ObjectId = Schema(None, alias="refrence_id")
    exec_status: Optional[ExecutionStatus] = ExecutionStatus.UNKNOWN
    tool: ToolInResp = Schema(None, alias="tool")
    build_id: ObjectIdInRes = Schema(None, alias="_build_id")
    tool_id:  ObjectIdInRes = Schema(None, alias="_tool_id")

    # image_name: Optional[ str]
    # tag_name: Optional[ ObjectIdInRes]


class BuildExecutorDeploymentStructure(BaseModel):
    image_name: str
    id: ObjectIdInRes
    tag_name: ObjectIdInRes



class BuildExecutorProgressResponse(BaseModel):
    exec_status: ExecutionStatus = ExecutionStatus.COMPLETED
    poll_after: int = 1000  # Milliseconds
    poll_again: Optional[bool] = True

    @validator('poll_again', always=True)
    def build_optional_fields(cls, v, values):
        cls.poll_after = 1000
        exec_status :  ExecutionStatus = values["exec_status"]

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
