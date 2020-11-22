from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.asset_schema import (
    IosAssetSchema, IosdAssetSchemaResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name, 
    asset_ios_collection_name as asset_collection,
)

# Domain
async def create_ios_asset(client: AsyncIOMotorClient, asset: IosAssetSchema) -> IosdAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    row = await collection_asset.update_one({"value":  asset.value},  {"$setOnInsert":   asset.dict()}, upsert=True)

    upserted_id = row.upserted_id
    if upserted_id == None :
        raise ValueError("iOS app already exists",asset.value)

    return await collection_asset.find_one({"value":  asset.value })
    


async def get_ios_asset(client: AsyncIOMotorClient, id: str) -> IosdAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    field_data = await collection_asset.find_one({"_id": id})
    field_data = IosdAssetSchemaResponse(**field_data)
    return field_data


async def get_all_ios_asset(client: AsyncIOMotorClient) -> List[IosdAssetSchemaResponse]:

    collection_asset = client[database_name][asset_collection]
    rows = collection_asset.find({})

    result: List[IosdAssetSchemaResponse] = []

    async for row in rows:
        result.append(
            IosdAssetSchemaResponse
            (
                **row
            )
        )
    return result
