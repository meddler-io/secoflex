from typing import Optional , List
from .dbmodel import DBModelMixin
from ..core.jwt import create_access_token, get_file_from_token

from .rwmodel import RWModel

class BaseFieldSchema(RWModel , DBModelMixin):
    field_id: str
    field_name: str
    field_etadata: List[str]
    field_tags: List[str]
    public: bool
    archived: bool
    version: int
