

from typing import List, Optional
from pydantic import BaseModel
from pydantic.fields import Schema


class DockerImageSpec(BaseModel):
    AttachStderr: Optional[bool] = Schema(None, alias="AttachStderr")
    AttachStdin: Optional[bool] = Schema(None, alias="AttachStdin")
    AttachStdout: Optional[bool] = Schema(None, alias="AttachStdout")
    Cmd: Optional[List[str]] = Schema(None, alias="Cmd")
    Domainname: Optional[str] = Schema(None, alias="Domainname")
    Entrypoint: Optional[List[str]] = Schema(None, alias="Entrypoint")
    Env: Optional[List[str]] = Schema(None, alias="Env")
    Hostname: Optional[str] = Schema(None, alias="Hostname")
    Image: Optional[str] = Schema(None, alias="Image")
    User: Optional[str] = Schema(None, alias="User")
    WorkingDir: Optional[str] = Schema(None, alias="WorkingDir")
    ArgsEscaped: Optional[bool] = Schema(None, alias="ArgsEscaped")
    NetworkDisabled: Optional[bool] = Schema(None, alias="NetworkDisabled")
    StopSignal: Optional[str] = Schema(None, alias="StopSignal")
    Shell: Optional[List[str]] = Schema(None, alias="Shell")

    
    



