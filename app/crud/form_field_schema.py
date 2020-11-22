from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.form_field_schema import (
  FormFieldSchemaDraft , BaseFieldSchema, FormFieldSchemaUpdate , FormFieldScheProperties
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, form_field_schema_collection_name, forms_schema_collection_name




async def create_draft_form_field_schema(client: AsyncIOMotorClient, form_field_schema_draft: FormFieldSchemaDraft , form_id: str) -> FormFieldSchemaDraft:

    collection_form_schema = client[database_name][forms_schema_collection_name]
    collection_form_field_schema = client[database_name][form_field_schema_collection_name]

    response = None

    async with await client.start_session() as s:
        # Note, start_transaction doesn't require "await".
        async with s.start_transaction():
            row =  await collection_form_field_schema.insert_one( form_field_schema_draft.dict() , session=s)
            form_field_inserted_id = row.inserted_id
            print("form_field_inserted_id" , form_field_inserted_id, form_id)
            row = await collection_form_schema.update_one({ "form_id": form_id } , {   "$push":  { "field": form_field_schema_draft.field_id }  }, session=s, upsert=True)
            modified_count = row.modified_count
            print("modified count", modified_count)
            if not modified_count == 1:
              s.abort_transaction()
              raise Exception("Transaction incomplete")

            
            inserted_field  =  await collection_form_field_schema.find_one( { "_id": form_field_inserted_id } , session=s) 
            response = FormFieldSchemaDraft( **inserted_field  )

        
    return response


async def get_form_field_schema(client: AsyncIOMotorClient, field_id: str) -> FormFieldSchemaDraft:

    collection_form_field_schema = client[database_name][form_field_schema_collection_name]
    field_data  =  await collection_form_field_schema.find_one( { "field_id": field_id } ) 
    return FormFieldSchemaDraft( **field_data  )


async def update_form_field_schema(client: AsyncIOMotorClient , field_id : str , updaed_field_data : FormFieldSchemaUpdate) -> FormFieldSchemaDraft:

    collection_form_field_schema = client[database_name][form_field_schema_collection_name]
    await collection_form_field_schema.update_one( { "field_id": field_id }, { "$set": updaed_field_data.dict(exclude_unset=True) }  ) 
    return await get_form_field_schema( client, field_id  )

async def set_form_field_properties(client: AsyncIOMotorClient , field_id : str , updaed_field_data : List[FormFieldSchemaUpdate] ) -> FormFieldSchemaDraft:


    _updaed_field_data = list()
    for doc in updaed_field_data:
        _updaed_field_data.append( doc.dict( exclude_unset = True ) )

    collection_form_field_schema = client[database_name][form_field_schema_collection_name]
    await collection_form_field_schema.update_one( { "field_id": field_id }, { "$set": { "properties": _updaed_field_data  } }  ) 
    return await get_form_field_schema( client, field_id  )




async def delete_form_field_schema(client: AsyncIOMotorClient , field_id : str , form_id : str) :

    collection_form_schema = client[database_name][forms_schema_collection_name]
    result  = await collection_form_schema.update_one( { "form_id": form_id }, { "$pull": { "field": field_id } }  ) 
    if not result.modified_count == 1:
              return {"updated": False}

    return {"updated": True}



