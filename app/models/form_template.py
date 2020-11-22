from typing import Optional , List
from .dbmodel import DBModelMixin
from ..core.jwt import create_access_token, get_file_from_token
from .form_field_schema import BaseFieldSchema
from .rwmodel import RWModel

class BaseFormTemplate(RWModel , DBModelMixin):
    form_schema_id: str
    form_name: str
    form_metadata: List[str] = []
    keywords: List[str] = []
    form_tags: List[str] = []
    public: bool
    archived: bool
    version: int
