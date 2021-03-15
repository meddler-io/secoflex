
from motor.frameworks.asyncio import pymongo_class_wrapper
from app.api.api_v2.endpoints import job
from typing import Any, List
from app.models.tool.job import JobInDb, JobInRequest, JobInResponse, JobProgressResponse, JobUpdateModel


from app.models.mongo_id import ObjectIdInReq, ObjectIdInRes, BsonObjectId
from app.models.tool.builds import BuildMessageSpec
from app.models.tool.build.common import BaseBuildModel, BaseBuildModelInRequest, BaseBuildModelInResponse, BaseBuildWithToolModelInResponse, BuildType

from app.models.tool.executor import BuildExecutorCompositeInResponse, BuildExecutorDeploymentStructure, BuildExecutorInDb, BuildExecutorInRequest, BuildExecutorInResponse, ExecutionStatus


from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    job_collection_name as coll_name,
    tools_collection_name,
    build_collection_name,
    build_executor_collection_name

)


async def create_job(client: AsyncIOMotorClient, job:  JobInRequest) -> JobInResponse:
    collection = client[database_name][coll_name]
    data = job.dict()
    data = JobInDb(**data).dict()
    result = await collection.insert_one(data)
    result = await collection.find_one({"_id": result.inserted_id})
    result = JobInResponse(**result)
    return result


async def update_job(client: AsyncIOMotorClient, job_id: str, job:  JobUpdateModel, exec_status: ExecutionStatus) -> JobInResponse:
    collection = client[database_name][coll_name]
    job_id = BsonObjectId(job_id)
    job.exec_status = exec_status

    result = await collection.update_one({"_id": job_id},  {"$set": job.dict()})
    result = await collection.find_one({"_id": job_id})
    result = JobInResponse(**result)
    return result


# JobInResponse
async def get_jobs(client: AsyncIOMotorClient, id: str) -> List[JobInResponse]:

    collection = client[database_name][build_collection_name]
    result:  List[Any] = []
    rows = collection.aggregate([

        {
            "$match": {
                "refrence_id": BsonObjectId(id)
            }
        },

        {
            "$lookup": {
                "from": build_executor_collection_name,
                "localField": "_id",
                "foreignField": "refrence_id",
                "as": "executors"
            }
        },

        {
            "$unwind": "$executors"
        },
        {
            "$project": {
                "_id": "$executors._id",
            }
        },
        {
            "$lookup": {
                "from": coll_name,
                "localField": "_id",
                "foreignField": "refrence_id",
                "as": "job"
            }
        },
        {
            "$unwind": "$job"
        },
        {
            "$replaceRoot":
            {
                "newRoot": "$job"
            }
        },
        {"$sort": {"_id": -1}}


    ])
    async for row in rows:
        row = JobInResponse(**row)
        result.append(row)

    return result


# JobInResponse
async def get_al_jobs(client: AsyncIOMotorClient) -> List[JobInResponse]:

    collection = client[database_name][build_collection_name]
    result:  List[Any] = []
    rows = collection.aggregate([

    

        {
            "$lookup": {
                "from": build_executor_collection_name,
                "localField": "_id",
                "foreignField": "refrence_id",
                "as": "executors"
            }
        },

        {
            "$unwind": "$executors"
        },
        {
            "$project": {
                "_id": "$executors._id",
            }
        },
        {
            "$lookup": {
                "from": coll_name,
                "localField": "_id",
                "foreignField": "refrence_id",
                "as": "job"
            }
        },
        {
            "$unwind": "$job"
        },
        {
            "$replaceRoot":
            {
                "newRoot": "$job"
            }
        },
        {"$sort": {"_id": -1}}


    ])
    async for row in rows:
        row = JobInResponse(**row)
        result.append(row)

    return result


async def get_job_status(client: AsyncIOMotorClient, job_id: str) -> JobProgressResponse:

    job_id = BsonObjectId(job_id)
    collection = client[database_name][coll_name]
    result = await collection.find_one({"_id": job_id})
    return JobProgressResponse(**result)
