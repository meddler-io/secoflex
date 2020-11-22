from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.asset_schema import (
    DomainAssetSchema, DomainAssetSchemaResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name, 
    asset_domain_collection_name as asset_collection,
)

# Domain
async def create_domain_asset(client: AsyncIOMotorClient, asset: DomainAssetSchema) -> DomainAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    row = await collection_asset.update_one({"value":  asset.value},  {"$setOnInsert":   asset.dict()}, upsert=True)

    upserted_id = row.upserted_id
    if upserted_id == None :
        raise ValueError("Domain already exists",asset.value)

    return await collection_asset.find_one({"value":  asset.value })
    


async def get_domain_asset(client: AsyncIOMotorClient, id: str) -> DomainAssetSchemaResponse:

    collection_asset = client[database_name][asset_collection]
    field_data = await collection_asset.find_one({"_id": id})
    field_data = DomainAssetSchemaResponse(**field_data)
    return field_data


async def get_all_domain_asset(client: AsyncIOMotorClient) -> List[DomainAssetSchemaResponse]:

    collection_asset = client[database_name][asset_collection]
    rows = collection_asset.find({})

    result: List[DomainAssetSchemaResponse] = []

    async for row in rows:
        result.append(
            DomainAssetSchemaResponse(
                **row
            )
        )
    return result
