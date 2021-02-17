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
from ..mongo_id import ObjectId



class BuildExecutorInBase(BuildMessageSpec):
    pass

class BuildExecutorInRequest(BuildExecutorInBase):
    pass

class BuildExecutorInDb(BuildExecutorInBase):
    refrence_id:  ObjectId
    pass

class BuildExecutorInResponse(BuildExecutorInBase):
    refrence_id:  Any
    
    pass
