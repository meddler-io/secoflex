from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.form_schema import (
    BaseFormSchema, FormSchemaDraft, FormSchemaDraft, FormSchemaDraftInResponse, FormSchemaListResponse, FormSchemaInResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, forms_schema_collection_name




async def create_draft_form_schema(conn: AsyncIOMotorClient, form_schema_draft: FormSchemaDraft) -> FormSchemaDraftInResponse:
    row = await conn[database_name][forms_schema_collection_name].insert_one(form_schema_draft.dict())
    row = await conn[database_name][forms_schema_collection_name].find_one( {"_id": row.inserted_id} )
    return FormSchemaDraftInResponse(**row)


async def get_draft_form_schema(conn: AsyncIOMotorClient ) -> FormSchemaListResponse:
    cursor = conn[database_name][forms_schema_collection_name].find( {} )
    form_schemas  : List[FormSchemaDraft] = []


    for form_data in  await cursor.to_list(length=100):
        form_schemas.append( FormSchemaDraftInResponse(**form_data)  )
    # ord("form_schemas",form_schemas)
    return FormSchemaListResponse(form_schemas=form_schemas) 

async def get_form_schema_by_id(conn: AsyncIOMotorClient, form_id: str ) -> FormSchemaInResponse:
    # row = await conn[database_name][forms_schema_collection_name].find_one( {"form_id", form_id} )
    row = await conn[database_name][forms_schema_collection_name].find_one( { "form_id": form_id} )
    return FormSchemaInResponse (**row ) 



