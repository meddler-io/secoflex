from typing import Optional, List, Dict
from pydantic.fields import Field
from pydantic.types import Any, constr
from enum import Enum
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from ..mongo_id import ObjectId



class BaseTool(BaseModel):
    name: str = ""
    alias: constr(regex=r'[a-z0-9]+(?:[._-]{1,2}[a-z0-9]+)*') = ""
    description: str = ""
    tags: List[str] = list()
    metadata: Dict = dict()
    # version: int



class ToolInDB(BaseTool):
    doc: Optional[datetime] = datetime.utcnow()
    dou: Optional[datetime] = datetime.utcnow()
    alias: str = "alias"
    active: bool = True


class ToolInReq(BaseTool):
    name: str = ""
    description: str = ""


class ToolInResp(BaseTool):
    id: ObjectId = Field(..., alias='_id')
    pass
