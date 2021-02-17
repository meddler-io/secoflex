from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.tool.tool import (
    ToolInDB, ToolInReq, ToolInResp
)


from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    tools_collection_name as coll_name,

)


# Tool
async def create_tool(client: AsyncIOMotorClient, tool: ToolInReq) -> ToolInResp:

    collection_asset = client[database_name][coll_name]
    row = await collection_asset.insert_one(ToolInDB(**tool.dict()).dict())
    inserted_id = row.inserted_id
    if inserted_id == None:
        raise ValueError("Unable to create tool")

    field_data = await collection_asset.find_one({"_id":  inserted_id})
    return field_data


async def get_tool(client: AsyncIOMotorClient, id: str) -> ToolInResp:
    collection_asset = client[database_name][coll_name]
    field_data = await collection_asset.find_one({"_id": ObjectId(id)})
    return field_data


async def get_tools(client: AsyncIOMotorClient) -> List[ToolInResp]:

    collection_asset = client[database_name][coll_name]
    rows = collection_asset.find({})

    result: List[ToolInResp] = []
    async for row in rows:
        result.append(row)
    return result

