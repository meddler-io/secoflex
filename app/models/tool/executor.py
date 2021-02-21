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
    pass


class BuildExecutorInRequest(BuildExecutorInBase):
    refrence_id: ObjectIdInReq = Schema(None, alias="refrence_id")
    exec_status: Optional[ExecutionStatus] = ExecutionStatus.UNKNOWN



class BuildExecutorInDb(BuildExecutorInBase):
    refrence_id: ObjectId = Schema(None, alias="refrence_id")
    exec_status: ExecutionStatus = ExecutionStatus.ENQUEUED



class BuildExecutorInResponse(BuildExecutorInBase):
    refrence_id: ObjectId = Schema(None, alias="refrence_id")
    exec_status: Optional[ExecutionStatus] = ExecutionStatus.UNKNOWN

    pass
