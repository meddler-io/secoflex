from typing import Optional , List
from .dbmodel import DBModelMixin
from ..core.jwt import create_access_token, get_file_from_token

from .rwmodel import RWModel

class BaseReportSchema(RWModel , DBModelMixin):
    active: bool
    template: str
    variables: List[str]

