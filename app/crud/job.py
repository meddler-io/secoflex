from app.models.dbmodel import ObjectId
from typing import List
from app.models.tool.job import JobInDb, JobInRequest, JobInResponse, JobUpdateModel
from app.models.tool.integrated.docker_build import DockerImageSpec
from app.models.mongo_id import ObjectIdInReq, ObjectIdInRes, BsonObjectId
from app.models.tool.builds import BuildMessageSpec
from app.models.tool.build.common import BaseBuildModel, BaseBuildModelInRequest, BaseBuildModelInResponse, BaseBuildWithToolModelInResponse, BuildType

from app.models.tool.executor import BuildExecutorCompositeInResponse, BuildExecutorDeploymentStructure, BuildExecutorInDb, BuildExecutorInRequest, BuildExecutorInResponse, ExecutionStatus


from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    job_collection_name as coll_name

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


async def get_jobs(client: AsyncIOMotorClient) -> List[JobInResponse]:

    collection = client[database_name][coll_name]
    result:  List[JobInResponse] = []
    rows = collection.aggregate([


    ])

    async for row in rows:

        result.append(JobInResponse(**row))

    return result
