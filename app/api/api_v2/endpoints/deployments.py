from app.models.dbmodel import ObjectId
from engine.integrations.services.build import parseBuild
from fastapi.params import Query
from app.models.tool.deployments import GenerateJobId, GetBuilExecutordIdFromJobId, GetToolIdFromJobId, JobModel
from engine.integrations.services.provider.provider import Provider
from app.crud.builds import create_build_executor, get_all_build_executor_for_image_tags, get_build, get_build_by_refrence_id, get_build_config, get_build_executor, get_build_executor_for_image_tag
from pathlib import PurePath
from ....core.config import DOCKER_API_CATALOG, DOCKER_DEFAULT_NAMESPACE, DOCKER_ENDPOINT, FAILURE_EXECUTION_WEBHOOK, FILESTORAGE_PATH, SUCCESS_EXECUTION_WEBHOOK
from typing import Any, Optional, List
from ....core.utils import save_upload_file
from fastapi import APIRouter, Body, Depends, HTTPException
from ....db.mongodb import AsyncIOMotorClient, get_database
from starlette.responses import FileResponse
from ....models.tool.tool import ToolInReq, ToolInResp, ToolModifyInReq
from ....crud.tools import edit_tool, get_tool, get_tools, create_tool
import requests
from typing import Dict
from engine.integrations import rmq
import asyncio
import requests
import json


router = APIRouter()

# deployment


@router.post("/deployment/service",
             tags=["deploymentl"],
             )
async def api_get_deployment_service(
        deployment_id: str = Body(..., embed=True),

        db: AsyncIOMotorClient = Depends(get_database),

):

    # result = await get_tool(db, tool_id)
    provider = Provider()
    result = provider.getDeployment(deployment_id)

    build_id = GetBuilExecutordIdFromJobId(deployment_id)
    build_details = await get_build_by_refrence_id(db, build_id)

    print('build_details', build_id, build_details)

    Config = build_details
    Config.id = build_id

    BuildDetails = build_details
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

    result = JobModel(
        **result, BuildDetails=BuildDetails.dict(), JobConfig=Config.dict())

    return result
    return Config


@router.get("/deployment/services/{tool_id}",
            tags=["deploymentl"],
            )
async def api_get_deployment_services(
        tool_id: str,
        db: AsyncIOMotorClient = Depends(get_database),

):

    result = await get_tool(db, tool_id)
    provider = Provider()
    # result = provider.searchDeployments(result.alias + ":")
    result = provider.searchDeployments(tool_id)
    return result


@router.delete("/deployment/service",
               tags=["deploymentl"],
               )
async def api_get_deployment_services(
        job_id: str,
        db: AsyncIOMotorClient = Depends(get_database),

):

    provider = Provider()
    result = provider.deleteDeployment(job_id)
    return result


@router.delete("/deployment/purge",
               tags=["deploymentl"],
               )
async def api_purge_deployment_services(
        db: AsyncIOMotorClient = Depends(get_database),

):

    provider = Provider()
    result = provider.purge()
    return result


@router.post("/deployment/run",
             tags=["deploymentl"],
             )
async def run_deployment_service(
        job_id: str = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),

):

    build_id = GetBuilExecutordIdFromJobId(job_id)
    tool_id = GetToolIdFromJobId(job_id)
    #

    Config = await get_build_by_refrence_id(db, build_id)
    # Config.id = "nomad_test"
    result = await asyncio.wait_for(rmq.RMQ.publish(job_id,  Config.json()), timeout=10)

    return result

    try:

        Config = await get_build_executor(db, build_id)
        Config.id = job_id
        Config.cmd = "echo"
        Config.success_endpoint = SUCCESS_EXECUTION_WEBHOOK % Config.id
        Config.failure_endpoint = FAILURE_EXECUTION_WEBHOOK % Config.id
        Config.config.system["input_dir"] = "/tmp"
        Config.config.system["base_path"] = "/tmp"
        Config.config.system["exec_timeout"] = "20000"

        Config.substitute_var = True
        Config.variables = {
            "input_dir": "$input_dir"
        }
        Config.dependencies = [

        ]

        Config.args = [

        ]

        print("SUCCESS_EXECUTION_WEBHOOK", Config.success_endpoint)
        print("FAILURE_EXECUTION_WEBHOOK", Config.failure_endpoint)

        # result = await rmq.RMQ.publish("tasks_test",  Config.json() )
        # print('result', result)
        print("Config", Config.json())
        result = await asyncio.wait_for(rmq.RMQ.publish(job_id,  Config.json()), timeout=10)

        return Config
    except Exception as err:
        raise err

    #

    result = await asyncio.wait_for(rmq.RMQ.publish(job_id,  {

        "id": "nomad_id",
        "environ": {

        },
        "entrypoint":  ["echo"],
        "cmd": "echo",
        "args": [],
        "substitute_var": True,
        "variables": {},
        "config": {

            "process": {},
            "reserved": {},
            "system": {},
        },
        "success_endpoint": "success_endpoint",
        "failure_endpoint": "failure_endpoint",


    }), timeout=10)

    return {"messasge": f"Running  {job_id}", "build_id": build_id, "tool_id": tool_id, "result": result

            }


@router.post("/deployment/service/{build_executor_id}",
             tags=["deploymentl"],
             )
async def api_create_deployment_service(
        build_executor_id: str,
        db: AsyncIOMotorClient = Depends(get_database),

):

    image_struct = await get_build_executor_for_image_tag(db, build_executor_id)
    image_name = image_struct.image_name
    tag_name = image_struct.tag_name

    provider = Provider()
    result = provider.createDeployment(
        GenerateJobId(image_struct.id, tag_name),
        f"{image_name}", f"rounak316/{image_name}", f"{tag_name}")
    return result


@router.get("/deployment/images/{tool_id}",
            tags=["deploymentl"],
            )
async def api_get_deployment_images(
        tool_id: str,
        db: AsyncIOMotorClient = Depends(get_database),

):

    return requests.get(DOCKER_API_CATALOG).json()


@router.get("/deployment/images/tags/{tool_id}",
            tags=["deploymentl"],
            )
async def api_get_deployment_images(
        tool_id: str,
        db: AsyncIOMotorClient = Depends(get_database),

):

    try:
        data = await get_tool(db, tool_id)
        image_name = f"{DOCKER_DEFAULT_NAMESPACE}/{data.alias}"
        DOCKER_API_TAGS = f"http://{DOCKER_ENDPOINT}/v2/{image_name}/tags/list"
        print(DOCKER_API_TAGS)
        tags = requests.get(DOCKER_API_TAGS).json()["tags"]
        return await get_all_build_executor_for_image_tags(db, tool_id, tags)

    except Exception as err:
        raise err
        return []


@router.post("/deployment/images/{image_id}",
             tags=["deploymentl"],
             )
async def api_deploy_image(
        image_id: str,
        db: AsyncIOMotorClient = Depends(get_database),

):

    return []
