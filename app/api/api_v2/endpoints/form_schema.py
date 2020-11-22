from typing import Optional, List
from ....core.utils import save_upload_file
from fastapi import APIRouter, Body, Depends ,HTTPException
from fastapi import FastAPI, File, UploadFile, Query
from ....core.jwt import get_current_user_authorizer
from ....db.mongodb import AsyncIOMotorClient, get_database
from starlette.responses import FileResponse
from ....models.form_schema import FormSchemaDraft, FormSchemaDraftInResponse, FormSchemaListResponse, FormSchemaInResponse
from ....crud.form_schema import create_draft_form_schema, get_draft_form_schema, get_form_schema_by_id

router = APIRouter()
from ....core.config import FILESTORAGE_PATH

from pathlib import PurePath

# Create & Draft a form schema
@router.post("/form/schema", response_model=FormSchemaDraftInResponse, tags=["form schema"])
async def Create_form_schema(
            form_schema_draft: FormSchemaDraft = Body(...,),
            db: AsyncIOMotorClient = Depends(get_database),
        ):

    form_schema_draft.create_form_id()
    file_in_response = await create_draft_form_schema(db ,form_schema_draft)
    return file_in_response


# Get Form schemas
@router.get("/form/schema" , response_model= FormSchemaListResponse , tags=["form schema"])
async def Get_form_schema(
            db: AsyncIOMotorClient = Depends(get_database),
        ):

    response =  await get_draft_form_schema(db )
    return response


# Get Form schemas
@router.get("/form/schema/{form_id}" , response_model= FormSchemaInResponse , tags=["form schema"])
async def Get_form_schema_by_id(
            form_id: str,
            db: AsyncIOMotorClient = Depends(get_database),
        ):
    response =  await get_form_schema_by_id( form_id= form_id , conn= db  )

    return response

