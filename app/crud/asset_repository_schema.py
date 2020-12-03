from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.asset_schema import (
    RepositoryAssetSchema, RepositoryAssetSchemaResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    asset_repository_collection_name as asset_collection,
)

# Domain


async def create_repository_asset(client: AsyncIOMotorClient, asset: RepositoryAssetSchema) -> RepositoryAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    row = await collection_asset.update_one({"url":  asset.url },  {"$setOnInsert":   asset.dict()}, upsert=True)

    upserted_id = row.upserted_id
    if upserted_id == None:
        raise ValueError("Repository already exists")

    field_data = await collection_asset.find_one({"url":  asset.url})
    field_data = RepositoryAssetSchemaResponse(**field_data)

    return field_data


async def get_repository_asset(client: AsyncIOMotorClient, id: str) -> RepositoryAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    field_data = await collection_asset.find_one({"_id": id})
    field_data = RepositoryAssetSchemaResponse(**field_data)
    return field_data


async def get_all_repository_asset(client: AsyncIOMotorClient) -> List[RepositoryAssetSchemaResponse]:

    collection_asset = client[database_name][asset_collection]
    rows = collection_asset.find({})

    result: List[RepositoryAssetSchemaResponse] = []

    async for row in rows:
        result.append(
            RepositoryAssetSchemaResponse(
                **row
            )
        )
    return result
