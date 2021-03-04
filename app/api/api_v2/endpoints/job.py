
from app.models.tool.executor import ExecutionStatus
from typing import Any, Optional
import json
from pydantic.types import Json
from app.models.mongo_id import ObjectId
from app.core.config import FAILURE_EXECUTION_WEBHOOK, JOB_FAILURE_EXECUTION_WEBHOOK, JOB_SUCCESS_EXECUTION_WEBHOOK, SUCCESS_EXECUTION_WEBHOOK
import asyncio
from app.models.tool.builds import BuildMessageSpec
from app.crud.builds import get_build_by_refrence_id
from app.models.tool.deployments import GetBuilExecutordIdFromJobId, GetToolIdFromJobId
from app.models.tool.job import JobInRequest, JobRequestModel, JobUpdateModel
from app.crud.job import create_job, get_jobs, update_job
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from ....db.mongodb import AsyncIOMotorClient, get_database
from engine.integrations import rmq


router = APIRouter()

# job


@router.post("/job/exec/{job_id}",
             tags=["job"],
             )
async def api_create_job(
        job_id: str,
        job_config: BuildMessageSpec = Body,
        db: AsyncIOMotorClient = Depends(get_database),

):

    build_id = GetBuilExecutordIdFromJobId(job_id)
    tool_id = GetToolIdFromJobId(job_id)
#
    Config = await get_build_by_refrence_id(db, build_id)
    Config = BuildMessageSpec(**Config.dict())

    Config = job_config

    result = JobInRequest(refrence_id=ObjectId(build_id), request=JobRequestModel(
        job_config=Config.dict()).dict(), )

    result = await create_job(db, result)

    Config = result.request.job_config
    Config.id = result.id

    build_details = await get_build_by_refrence_id(db, build_id)

    build_details = build_details.result

    Config.cmd = build_details.Cmd
    Config.entrypoint = build_details.Entrypoint

    embedded_env = build_details.Env
    for env in embedded_env:
        env = env.split("=", 2)
        if len(env) == 2:
            Config.config.reserved[env[0]] = env[1]
        elif len(env) == 1:
            Config.config.reserved[env[0]] = ""

    Config.success_endpoint = JOB_SUCCESS_EXECUTION_WEBHOOK % Config.id
    Config.failure_endpoint = JOB_FAILURE_EXECUTION_WEBHOOK % Config.id

    result = await asyncio.wait_for(rmq.RMQ.publish(job_id,  Config.json()), timeout=10)
    return Config


@router.get("/job",
            tags=["job"],
            )
async def api_get_jobs(
        db: AsyncIOMotorClient = Depends(get_database),

):
    result = await get_jobs(db)

    return result


# Webhooks

@router.post("/job/result/success/{job_id}",
             tags=["job"],
             )
async def api_webhook_succes_job(
        job_id: str,
        result: Request,
        db: AsyncIOMotorClient = Depends(get_database),

):
    result = await result.body()
    try:
        result = json.loads(result.decode('utf8'))
    except:
        pass
    result = JobUpdateModel(response=result)
    result = await update_job(db, job_id,  result, ExecutionStatus.FAILURE)
    return result


@router.post("/job/result/failure/{job_id}",
             tags=["job"],
             )
async def api_webhook_failure_job(
        job_id: str,
        result: Request,
        db: AsyncIOMotorClient = Depends(get_database),

):
    result = await result.body()
    try:
        result = json.loads(result.decode('utf8'))
    except:
        pass

    result = JobUpdateModel(response=result)
    result = await update_job(db, job_id,  result, ExecutionStatus.FAILURE)
    return result
