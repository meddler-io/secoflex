from typing import Optional, List
from ....core.utils import save_upload_file
from fastapi import APIRouter, Body, Depends ,HTTPException
from fastapi import FastAPI, File, UploadFile, Query
from ....core.jwt import get_current_user_authorizer
from ....db.mongodb import AsyncIOMotorClient, get_database
from starlette.responses import FileResponse
from ....models.form_field_schema import FormFieldSchemaDraft , FormFieldSchemaUpdate, FormFieldScheProperties
from ....crud.form_field_schema import create_draft_form_field_schema , get_form_field_schema , update_form_field_schema , delete_form_field_schema , set_form_field_properties

router = APIRouter()
from ....core.config import FILESTORAGE_PATH

from pathlib import PurePath

tags =  ["field schema"]

# Create & Draft a form schema
@router.post("/form/{form_id}/field/schema", response_model=FormFieldSchemaDraft, tags=tags)
async def Create_field_schema(
            form_id: str,
            form_field_schema_draft: FormFieldSchemaDraft = Body(...,),
            db: AsyncIOMotorClient = Depends(get_database),
        ):

    form_field_schema_draft.create_field_id()
    form_field_schema_draft_response = await create_draft_form_field_schema(db ,form_field_schema_draft , form_id)
    return form_field_schema_draft_response



@router.delete("/form/{form_id}/field/{field_id}", tags=tags)
async def Delete_field_schema(
            form_id: str,
            field_id: str,

            db: AsyncIOMotorClient = Depends(get_database),
        ):

    response = await delete_form_field_schema(db  ,field_id= field_id , form_id=form_id)
    return response



# Create & Draft a form schema
@router.get("/field/schema/{field_id}", response_model=FormFieldSchemaDraft, tags=tags)
async def Get_field_schema(
            field_id: str,
            db: AsyncIOMotorClient = Depends(get_database),
        ):

    form_field_schema_draft_response = await get_form_field_schema(db  , field_id)
    return form_field_schema_draft_response



# Create & Draft a form schema
@router.put("/field/schema/{field_id}", response_model=FormFieldSchemaDraft, tags=tags)
async def Update_field_schema(
            field_id: str,
            update_data: FormFieldSchemaUpdate,
            db: AsyncIOMotorClient = Depends(get_database),
        ):

    form_field_schema_draft_response = await update_form_field_schema(db  , field_id, update_data)
    return form_field_schema_draft_response



# Create & Draft a form schema
@router.post("/field/schema/properties/{field_id}", response_model=FormFieldSchemaDraft, tags=tags)
async def Update_field_properties(
            field_id: str,
             update_data:  List[FormFieldScheProperties] ,
            db: AsyncIOMotorClient = Depends(get_database),
        ):

    print("dsada")
    form_field_schema_draft_response = await set_form_field_properties(db  , field_id, update_data)
    return form_field_schema_draft_response




