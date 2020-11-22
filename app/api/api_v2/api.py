from fastapi import APIRouter

from .endpoints.file import router as file_router
from .endpoints.form_schema import router as form_router
from .endpoints.field_schema import router as form_field_router
from .endpoints.asset import router as asset_router


router = APIRouter()
router.include_router(file_router, prefix='/v2' )
router.include_router(form_router, prefix='/v2' )
router.include_router(form_field_router, prefix='/v2' )
router.include_router(asset_router, prefix='/v2' )
