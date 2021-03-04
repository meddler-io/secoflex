from fastapi import APIRouter

from .endpoints.file import router as file_router
from .endpoints.form_schema import router as form_router
from .endpoints.field_schema import router as form_field_router
from .endpoints.asset import router as asset_router
from .endpoints.test import router as test_router
from .endpoints.tools import router as tools_router
from .endpoints.builds import router as builds_router
from .endpoints.result import router as builds_result_router
from .endpoints.deployments import router as deployment_router
from .endpoints.job import router as job_router


router = APIRouter()
router.include_router(file_router, prefix='/v2')
router.include_router(form_router, prefix='/v2')
router.include_router(form_field_router, prefix='/v2')
router.include_router(asset_router, prefix='/v2')
router.include_router(tools_router, prefix='/v2')
router.include_router(builds_router, prefix='/v2')
router.include_router(builds_result_router, prefix='/v2')
router.include_router(deployment_router, prefix='/v2')
router.include_router(job_router, prefix='/v2')

# Test router
router.include_router(test_router)
