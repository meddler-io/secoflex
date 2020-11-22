from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.asset_schema import (
    AndroidAssetSchema, AndroidAssetSchemaResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name, 
    asset_android_collection_name as asset_collection,
)

# Domain
async def create_android_asset(client: AsyncIOMotorClient, asset: AndroidAssetSchema) -> AndroidAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    row = await collection_asset.update_one({"value":  asset.value},  {"$setOnInsert":   asset.dict()}, upsert=True)

    upserted_id = row.upserted_id
    if upserted_id == None :
        raise ValueError("Android app already exists",asset.value)

    return await collection_asset.find_one({"value":  asset.value })
    


async def get_android_asset(client: AsyncIOMotorClient, id: str) -> AndroidAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    field_data = await collection_asset.find_one({"_id": id})
    field_data = AndroidAssetSchemaResponse(**field_data)
    return field_data


async def get_all_android_asset(client: AsyncIOMotorClient) -> List[AndroidAssetSchemaResponse]:

    collection_asset = client[database_name][asset_collection]
    rows = collection_asset.find({})

    result: List[AndroidAssetSchemaResponse] = []

    async for row in rows:
        result.append(
            AndroidAssetSchemaResponse(
                **row
            )
        )
    return result
