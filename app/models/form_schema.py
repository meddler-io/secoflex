from typing import Optional , List
from pydantic.types import constr
from .dbmodel import DBModelMixin
from ..core.jwt import create_access_token, get_file_from_token
from .form_field_schema import BaseFieldSchema
from .rwmodel import RWModel

class BaseFormSchema(RWModel , DBModelMixin):
    form_id: str = ""
    form_name: str  = ""
    form_metadata: List[str] = []
    form_tags: List[str] = []
    field: List[str] = []
    public: bool = True
    draft: bool = True
    archived: bool = True
    version: int = 1


class FormSchemaDraft(RWModel):
    form_id: str = ""
    draft: bool = True
    form_name: constr(strip_whitespace=True, min_length=1)
    title: str = ""
    subtitle: str = ""

    def create_form_id(self):
        import uuid
        form_id = uuid.uuid4().hex
        self.form_id = form_id
        return form_id

class FormSchemaInResponse(BaseFormSchema):
    pass


class FormSchemaDraftInResponse(FormSchemaDraft):
    pass


class FormSchemaListResponse(RWModel):
    form_schemas: List[FormSchemaDraft]

