from app.models.mongo_id import ObjectIdInReq, ObjectIdInRes, BsonObjectId
from app.models.tool.builds import BuildMessageSpec
from app.models.tool.build.common import BaseBuildModel, BaseBuildModelInRequest, BaseBuildModelInResponse, BaseBuildWithToolModelInResponse, BuildType

from app.models.tool.executor import BuildExecutorInDb, BuildExecutorInRequest, BuildExecutorInResponse, ExecutionStatus
from logging import log
import logging
from typing import Any, List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime
from typing import Union
import pymongo


from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    build_collection_name as coll_name,
    tools_collection_name as tool_coll_name,
    build_executor_collection_name as exec_coll_name

)


# Build
# async def create_build(client: AsyncIOMotorClient, build_type: BuildType, build:  Union[RegistryPublicInReq, RegistryPrivateInReq]) -> Union[RegistryPublicInResp, RegistryPrivateInResp]:

#     collection = client[database_name][coll_name]

#     if build_type == BuildType.REGISTRY_PUBLIC:
#         data = RegistryPublicInDB(**build.dict()).dict()
#         result = await collection.insert_one(data)
#         return await collection.find_one({"_id": result.inserted_id})

#     elif build_type == BuildType.REGISTRY_PRIVATE:
#         data = RegistryPrivateInReq(**build.dict()).dict()
#         result = await collection.insert_one(data)
#         return await collection.find_one({"_id": result.inserted_id})

#     return {}

async def create_build(client: AsyncIOMotorClient, build:  Any) -> any:
    collection = client[database_name][coll_name]
    data = build.dict()
    data = BaseBuildModelInRequest(**data).dict(exclude_none=True)

    result = await collection.insert_one(data)
    result = await collection.find_one({"_id": result.inserted_id})
    print(result)
    result = BaseBuildModelInResponse(**data)
    return result


async def edit_build(client: AsyncIOMotorClient, id: str, build_data:  Any) -> any:
    id = ObjectId(id)
    collection = client[database_name][coll_name]
    data = BaseBuildModel(**build_data.dict()).dict(exclude_none=True)
    print(data)

    result = await collection.update_one({"_id": id},  {"$set": data})
    result = await get_build(client, id)
    return result

# Build


async def get_all_build(client: AsyncIOMotorClient, tool_id: str) -> Any:

    collection = client[database_name][coll_name]
    rows = collection.find({"refrence_id": ObjectId(tool_id)})

    result: List[BaseBuildModelInResponse] = []

    async for row in rows:
        row["_id"] = str(row["_id"])
        result.append(
            BaseBuildModelInResponse(**row)
        )

    return result


async def get_build(client: AsyncIOMotorClient, build_id: str) -> BaseBuildWithToolModelInResponse:

    build_id = ObjectId(build_id)
    collection = client[database_name][coll_name]
    result = await collection.find_one({"_id": ObjectId(build_id)})

    result = collection.aggregate([
        {
            "$match": {
                "_id": build_id
            }
        },
        {
            "$lookup": {
                "from": tool_coll_name,
                "localField": "refrence_id",
                "foreignField": "_id",
                "as": "tool"
            }
        },
        {
            "$set": {
                "tool": {"$arrayElemAt": ["$tool", 0]}
            }
        }

    ])

    async for r in result:
        result = r
        break
    else:
        raise Exception("Not found")
    # result = await result[0]
    result = BaseBuildWithToolModelInResponse(**result)
    return result


async def get_build_config(client: AsyncIOMotorClient, build_id: str) -> BuildMessageSpec:

    result = await get_build(client, build_id)
    result = result.build_config
    return result


async def update_build_config(client: AsyncIOMotorClient,  build_id: str, build_config: BuildMessageSpec) -> Any:

    collection = client[database_name][coll_name]
    result = await collection.update_one({"_id": ObjectId(build_id)},  {"$set": {"build_config": build_config.dict()}})

    result = await get_build(client, build_id)

    return result


# Build Executor
async def create_build_executor(client: AsyncIOMotorClient, build_id: str,  build_config: BuildMessageSpec) -> BuildExecutorInResponse:

    build_id = BsonObjectId(build_id)
    data = BuildExecutorInDb(
        **build_config.dict(),
    )
    data.refrence_id = build_id

    collection = client[database_name][exec_coll_name]
    result = await collection.insert_one(data.dict())
    inserted_id = result.inserted_id

    result = await collection.find_one({"_id": inserted_id})
    result = BuildExecutorInResponse(**result)
    return result

# Build Executor


async def get_all_build_executor(client: AsyncIOMotorClient, build_id: str) -> List[BuildExecutorInResponse]:

    collection = client[database_name][exec_coll_name]

    rows = collection.find({"refrence_id":   ObjectId(build_id)}, ).sort(
        [("_id", pymongo.DESCENDING)])

    result: List[BuildExecutorInResponse] = []

    async for row in rows:
        result.append(
            BuildExecutorInResponse(**row)
        )

    return result


async def get_build_executor(client: AsyncIOMotorClient, build_executor_id: str) -> List[BuildExecutorInResponse]:

    collection = client[database_name][exec_coll_name]
    result = await collection.find_one({"_id":  ObjectId(build_executor_id)}, )
    result = BuildExecutorInResponse(**result)

    return result


async def set_build_executor_status(client: AsyncIOMotorClient, build_executor_id: str, exec_status: ExecutionStatus) -> List[BuildExecutorInResponse]:

    collection = client[database_name][exec_coll_name]
    result = await collection.update_one(
        {"_id":  ObjectId(build_executor_id)},
        {
            "$set": {
                "exec_status": exec_status
            }
        }
    )

    return await get_build_executor(client, build_executor_id)
