from typing import Optional , List
from .dbmodel import DBModelMixin
from pydantic.types import constr , Any
from ..core.jwt import create_access_token, get_file_from_token
from enum import Enum, IntEnum
from .rwmodel import RWModel
from pydantic import  validator


class ComponentTypeEnum(str, Enum):
    IP_ADDRESS = 'ip_address',
    TEXT = 'text',
    RICH_TEXT = 'rich_text',
    BOOLEAN = 'boolean',
    ENUM = 'enum',
    FILE = 'file',
    IMAGE = 'image',
    VIDEO = 'video',
    SELECT = 'select',
    LIST = 'list',
    CODE = 'code',
    URL = 'url',
    CUSTOM_BUILDER = 'custom_form_builder'


# Sync with the frontend
class PropertyType(str, Enum):
    INPUT_TEXT = 'text',
    INPUT_TEXTAREA = 'textarea',
    INPUT_CHECKBOX = 'checkbox',
    INPUT_SELECT = 'select',
    INPUT_RADIO = 'radio',
    INPUT_MULTI_SELECT = 'multi_select',
    INPUT_IMAGE = 'image',
    INPUT_FILE = 'file',
    INPUT_THUMBNAIL = 'thumbnail',
    INPUT_ICON = 'icon',
    TOGGLE_SWITCH = 'toggle',
    CHIPS = 'chips',

class FormFieldScheProperties(DBModelMixin):
    property_tyoe: PropertyType
    property_name: str
    property_identifier: str
    property_default_value: Any
    property_label: Optional[str]
    property_icon: Optional[str]



class BaseFieldSchema(RWModel , DBModelMixin):
    field_id: str
    field_name: str
    component_type: str
    field_etadata: List[str]
    field_tags: List[str]
    public: bool
    archived: bool
    version: int
    published: bool = False
    required: bool
    draft: bool = True
    validatioon_pattern: str
    properties: Optional[ List[FormFieldScheProperties] ]



class FormFieldSchemaDraft(RWModel):
    field_id:str = ""
    subtitle: str = ""
    draft: bool = True
    component_type: ComponentTypeEnum
    published: bool = False
    properties: Optional[ List[FormFieldScheProperties] ]
    title: Optional[str]
    subtitle: Optional[str]
    identifier: Optional[str]
    placeholder: Optional[str]
    keywords: Optional[List[str]]

    def create_field_id(self):
        import uuid
        field_id = uuid.uuid4().hex
        self.field_id = field_id
        return field_id


class FormFieldSchemaUpdate(RWModel):
    identifier: Optional[constr(strip_whitespace=True, min_length=0)] = ""
    title: Optional[constr(strip_whitespace=True, min_length=1)] = ""
    subtitle: Optional[constr(strip_whitespace=True)] = ""
    placeholder: Optional[str]
    published: Optional[bool]
    keywords: Optional[List[str]]
    properties: Optional[ List[FormFieldScheProperties] ]




