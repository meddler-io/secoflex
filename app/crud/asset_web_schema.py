from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.asset_schema import (
    WebAssetSchema, WebAssetSchemaResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    asset_web_collection_name as asset_collection,
)

# Domain


async def create_web_asset(client: AsyncIOMotorClient, asset: WebAssetSchema) -> WebAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    row = await collection_asset.update_one({"value":  asset.value},  {"$setOnInsert":   asset.dict()}, upsert=True)

    upserted_id = row.upserted_id
    if upserted_id == None:
        raise ValueError("Domain already exists")

    field_data = await collection_asset.find_one({"value":  asset.value})
    field_data = WebAssetSchemaResponse(**field_data)

    return field_data


async def get_web_asset(client: AsyncIOMotorClient, id: str) -> WebAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    field_data = await collection_asset.find_one({"_id": id})
    field_data = WebAssetSchemaResponse(**field_data)
    return field_data


async def get_all_web_asset(client: AsyncIOMotorClient) -> List[WebAssetSchemaResponse]:

    collection_asset = client[database_name][asset_collection]
    rows = collection_asset.find({})

    result: List[WebAssetSchemaResponse] = []

    async for row in rows:
        result.append(
            WebAssetSchemaResponse(
                **row
            )
        )
    return result
