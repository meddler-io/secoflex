from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.asset_schema import (
    HostAssetSchema, HostAssetSchemaResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    asset_host_collection_name,
    asset_android_collection_name,
    asset_domain_collection_name,
    asset_ios_collection_name,
    asset_docker_collection_name,
    asset_repository_collection_name,
    asset_web_collection_name
)

# Host


async def create_host_asset(client: AsyncIOMotorClient, host_asset: HostAssetSchema) -> HostAssetSchemaResponse:

    collection_asset_host = client[database_name][asset_host_collection_name]
    # row = await collection_asset_host.insert_one(host_asset.dict())
    row = await collection_asset_host.update_one({"value":  host_asset.value},  {"$setOnInsert":   host_asset.dict()}, upsert=True)
    upserted_id = row.upserted_id
    if upserted_id == None :
        raise ValueError("Host already exists", host_asset.value)

    return await collection_asset_host.find_one({"value":  host_asset.value})


async def get_host_asset(client: AsyncIOMotorClient, id: str) -> HostAssetSchemaResponse:

    collection_form_field_schema = client[database_name][asset_host_collection_name]
    field_data = await collection_form_field_schema.find_one({"_id": id})
    field_data = HostAssetSchemaResponse(**field_data)
    return field_data


async def get_all_host_asset(client: AsyncIOMotorClient) -> List[HostAssetSchemaResponse]:

    collection_form_field_schema = client[database_name][asset_host_collection_name]
    rows = collection_form_field_schema.find({})

    result: List[HostAssetSchemaResponse] = []

    async for row in rows:
        result.append(
            HostAssetSchemaResponse(
                **row
            )
        )

    return result
