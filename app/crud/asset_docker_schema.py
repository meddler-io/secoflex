from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.asset_schema import (
    DockerAssetSchema, DockerAssetSchemaResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    asset_docker_collection_name as asset_collection,
)

# Domain


async def create_docker_asset(client: AsyncIOMotorClient, asset: DockerAssetSchema) -> DockerAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    row = await collection_asset.update_one({"url":  asset.url},  {"$setOnInsert":   asset.dict()}, upsert=True)

    upserted_id = row.upserted_id
    if upserted_id == None:
        raise ValueError("Repository already exists")

    field_data = await collection_asset.find_one({"url":  asset.url})
    field_data = DockerAssetSchemaResponse(**field_data)

    return field_data


async def get_docker_asset(client: AsyncIOMotorClient, id: str) -> DockerAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    field_data = await collection_asset.find_one({"_id": id})
    field_data = DockerAssetSchemaResponse(**field_data)
    return field_data


async def get_all_docker_asset(client: AsyncIOMotorClient) -> List[DockerAssetSchemaResponse]:

    collection_asset = client[database_name][asset_collection]
    rows = collection_asset.find({})

    result: List[DockerAssetSchemaResponse] = []

    async for row in rows:
        result.append(
            DockerAssetSchemaResponse(
                **row
            )
        )
    return result
