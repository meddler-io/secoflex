
from app.models.tool.builds import BuildMessageSpec
from app.models.tool.executor import BuildExecutorInRequest, BuildExecutorInResponse
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from pydantic.fields import Schema


class ResourceModel(BaseModel):
    CPU: int
    MemoryMB: int
    DiskMB: int
    IOPS: int


class TaskModel(BaseModel):
    Name: str
    Configuration: Any = Schema(..., alias="Config")

    Env: Dict[str, str]
    Resources: ResourceModel

    pass


class TaskGroupModel(BaseModel):
    Name: str
    Count: int
    Tasks: List[TaskModel]


class JobModel(BaseModel):
    Namespace: str
    Name: str
    TaskGroups: List[TaskGroupModel]
    Status: str
    SubmitTime: int
    JobConfig: BuildMessageSpec
    BuildDetails: Optional[ BuildExecutorInResponse ]


def GenerateJobId(tool_id: str, executir_id: str):
    return f"{tool_id}:{executir_id}"

def GetBuilExecutordIdFromJobId(job_id: str):
    return job_id.split(":")[1]

def GetToolIdFromJobId(job_id: str):
    return job_id.split(":")[0]
