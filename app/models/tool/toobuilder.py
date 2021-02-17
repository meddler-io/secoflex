from typing import Optional, List, Dict
from pydantic.fields import Field
from pydantic.types import Any
from enum import Enum
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from ..mongo_id import ObjectId



class BaseToolBuilder(BaseModel):
    name: str = ""
    alias: str = ""
    description: str = ""
    tags: List[str] = list()
    metadata: Dict = dict()



class ToolInDB(BaseToolBuilder):
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    alias: str = "alias"
    active: bool = True


class ToolInReq(BaseToolBuilder):
    name: str = ""
    description: str = ""


class ToolInResp(BaseToolBuilder):
    id: ObjectId = Field(..., alias='_id')
    pass
