from app.models.tool.executor import BuildExecutorInDb, BuildExecutorInRequest, BuildExecutorInResponse
from logging import log
import logging
from typing import Any, List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime
from typing import Union
import pymongo
from ..models.tool.builds import (
    BaseBuildInResponse, BuildConfig, BuildMessageSpec, BuildType,
    RegistryPrivateInReq, RegistryPrivateInResp, RegistryPublicInDB,
    RegistryPublicInResp, RegistryPublicInReq, BaseBuildType
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    build_collection_name as coll_name,
    build_executor_collection_name as exec_coll_name

)


# Build
async def create_build(client: AsyncIOMotorClient, build_type: BuildType, build:  Union[RegistryPublicInReq, RegistryPrivateInReq]) -> Union[RegistryPublicInResp, RegistryPrivateInResp]:

    collection = client[database_name][coll_name]

    if build_type == BuildType.REGISTRY_PUBLIC:
        data = RegistryPublicInDB(**build.dict()).dict()
        result = await collection.insert_one(data)
        return await collection.find_one({"_id": result.inserted_id})

    elif build_type == BuildType.REGISTRY_PRIVATE:
        data = RegistryPrivateInReq(**build.dict()).dict()
        result = await collection.insert_one(data)
        return await collection.find_one({"_id": result.inserted_id})

    return {}

# Build


async def get_all_build(client: AsyncIOMotorClient, tool_id: str) -> Any:

    collection = client[database_name][coll_name]
    rows = collection.find({"refrence_id": tool_id})

    result: List[RegistryPrivateInReq] = []

    async for row in rows:
        row["_id"] = str(row["_id"])
        result.append(
            row
        )

    return result


async def get_build(client: AsyncIOMotorClient, build_id: str) -> BaseBuildInResponse:

    collection = client[database_name][coll_name]
    result = await collection.find_one({"_id": ObjectId(build_id)})
    result = BaseBuildInResponse(**result)

    return result


async def get_build_config(client: AsyncIOMotorClient, build_id: str) -> BuildMessageSpec:

    result = await get_build(client, build_id)
    return result.build_config


async def update_build_config(client: AsyncIOMotorClient,  build_id: str, build_config: BuildMessageSpec) -> BaseBuildInResponse:

    collection = client[database_name][coll_name]
    result = await collection.update_one({"_id": ObjectId(build_id)},  {"$set": {"build_config": build_config.dict()}})

    result = await get_build(client, build_id)

    return result


# Build Executor
async def create_build_executor(client: AsyncIOMotorClient, build_id: str,  build_config: BuildExecutorInRequest) -> BuildExecutorInResponse:

    data = BuildExecutorInDb(**build_config.dict(),
                             refrence_id=ObjectId(build_id))
    collection = client[database_name][exec_coll_name]
    result = await collection.insert_one(data.dict())
    inserted_id = result.inserted_id

    result = await collection.find_one({"_id": inserted_id})

    inserted_id = str(inserted_id)

    result = BuildExecutorInResponse(**result)
    result.id = inserted_id
    return result

# Build Executor


async def get_all_build_executor(client: AsyncIOMotorClient, build_id: str) -> List[BuildExecutorInResponse]:

    collection = client[database_name][exec_coll_name]

    rows = collection.find({"refrence_id":   build_id}, ).sort(
        [("_id", pymongo.DESCENDING)])

    result: List[BuildExecutorInResponse] = []

    async for row in rows:
        row["_id"] = str(row["_id"])
        result.append(
            row
        )

    return result
