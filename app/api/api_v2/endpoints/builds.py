import traceback 
from engine.integrations.services.build import parseBuild
from app.models.tool.build.common import BaseBuildModel
from app.models.tool.build.bundle_upload import BundleUploadInBase
import asyncio
import json
from logging import log
from pathlib import PurePath
from ....core.config import FAILURE_EXECUTION_WEBHOOK, FILESTORAGE_PATH, SUCCESS_EXECUTION_WEBHOOK

from fastapi import APIRouter, Body, Depends
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.tool.builds import BuildMessageSpec
from ....crud.builds import create_build, create_build_executor, edit_build, get_all_build, get_all_build_executor, get_build, update_build_config, get_build_config
from engine.integrations import rmq
from bson import json_util
from engine.integrations.minio import generate_download_url, generate_upload_url
import uuid

#

from ....models.tool.build.bundle_url import BuildType, BundleUrlInReq
from ....models.tool.build.dockerfile import DockerfileUrlInReq
from ....models.tool.build.bundle_git import GitrlInReq
from ....models.tool.build.private_registry import DockerPrivaterlInReq
from ....models.tool.build.public_registry import DockerPublicrlInReq


router = APIRouter()

# Build


@router.put("/build/config/{id}", tags=["tool"])
async def api_update_build_config(
    id: str,
    build_config: BuildMessageSpec = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),
):
    try:
        result = await update_build_config(db,  id, build_config)
        return result
    except Exception as err:
        print(err)
        return False

    return True


@router.get("/build/config/{id}", tags=["tool"])
async def api_get_build_config(
    id: str,
    db: AsyncIOMotorClient = Depends(get_database),
):
    try:
        result = await get_build_config(db,  id)
        return result
    except Exception as err:
        return {"error": str(err)}


@router.get("/build/executors/{id}", tags=["tool"])
async def api_get_all_build_executor(
    id: str,
    db: AsyncIOMotorClient = Depends(get_database),
):
    response = await get_all_build_executor(db, id)
    return response


@router.get("/build/{tool_id}/{build_id}",
            #  response_model=Any],
            tags=["build"]
            )
async def api_get_build(
        tool_id: str,
        build_id: str,
        db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_build(db, build_id)
    return response


@router.get("/builds/{tool_id}",
            #  response_model=Any],
            tags=["build"]
            )
async def api_get_all_build(
        tool_id: str,
        db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_all_build(db, tool_id)
    return response


@router.post("/build/run/{id}", tags=["tool"])
async def api_run_build(
    id: str,
    db: AsyncIOMotorClient = Depends(get_database),
):
    try:
        result = await get_build(db,  id)
        result = parseBuild(result)
        build_config = await get_build_config(db,  id)

        Config = await create_build_executor(db, id, build_config)
        print("Tag", Config.id)
        Config.cmd = "/kaniko/executor"
        Config.success_endpoint = SUCCESS_EXECUTION_WEBHOOK % Config.id
        Config.failure_endpoint = FAILURE_EXECUTION_WEBHOOK % Config.id
        Config.config.system["input_dir"] = result["env"]["input_dir"]
        Config.config.system["base_path"] = result["env"]["base_path"]
        Config.config.system["exec_timeout"] = "20000"

        # Config.config.system["DOCKER_CONFIG"] = "/kaniko/fs/input/configmaps/"
        Config.environ["DOCKER_CONFIG"] = "$input_dir/configmaps/"

        # Substutute env variables
        for key in result["env"]:
            Config.environ[key] = result["env"][key]

        BuildContext = result["env"]["BUILDCONTEXT"]
        Config.substitute_var = True
        Config.variables = {
            "input_dir": "$input_dir"
        }
        Config.dependencies = [
            {
                "id": "uploadedbundles",
                "alias": "uploadedbundles",
                "type": "Type"
            },
            {
                "id": "configmaps",
                "alias": "configmaps",
                "type": "Type"
            }
        ]

        Config.args = ["--context=" + f"{BuildContext}",
                       f"--destination=192.168.29.5:5000/rounak316/hello:{Config.id}",
                       "--cache=false",
                       "--cleanup",



                       ]

        print("SUCCESS_EXECUTION_WEBHOOK", Config.success_endpoint)
        print("FAILURE_EXECUTION_WEBHOOK", Config.failure_endpoint)

        # result = await rmq.RMQ.publish("tasks_test",  Config.json() )
        # print('result', result)
        print("Config", Config.json())
        result = await asyncio.wait_for(rmq.RMQ.publish("tasks_test",  Config.json()), timeout=10)

        return Config

        # message = result.build_config.json()
        # message = result.json()
        config = await create_build_executor(db, id, result.build_config)

        config.success_endpoint = SUCCESS_EXECUTION_WEBHOOK % config.id
        config.failure_endpoint = FAILURE_EXECUTION_WEBHOOK % config.id

        print("SUCCESS_EXECUTION_WEBHOOK", config.success_endpoint)
        print("FAILURE_EXECUTION_WEBHOOK", config.failure_endpoint)

        await asyncio.wait_for(rmq.RMQ.publish("tasks_test",  config.json()), timeout=4)
        return config
    except Exception as err:
        print(err)
        traceback.print_exc() 
        return {"error": str(err)}

    return True


@router.post("/build/upload/init", tags=["tool"])
async def api_generate_upload_url(
    id:  str = Body(..., embed=True),
    filename: str = Body(..., embed=True),
    db: AsyncIOMotorClient = Depends(get_database),
):

    bucket_name = "uploadedbundles"
    version = uuid.uuid4().hex
    identifier = f"{id}/{version}:{filename}"
    url = generate_upload_url(bucket_name, identifier)

    return {
        "url": url,
        "filename": filename,
        "identifier": id,
        "bucket": bucket_name,
        "version": version
    }


@router.post("/build/download/init", tags=["tool"])
async def api_generate_upload_url(
    url:  str = Body(..., embed=True),
    filename:  str = Body(..., embed=True),
    identifier:  str = Body(..., embed=True),
    bucket:  str = Body(..., embed=True),
    version:  str = Body(..., embed=True),
):

    object = f"{identifier}/{version}:{filename}"
    url = generate_download_url(bucket, object)

    return {
        "url": url,

    }


#
# api_create_public_registry
@router.post("/build/" + BuildType.BUNDLE_UPLOAD.value, tags=["tool"])
async def api_create_bundle_upload(
    data:  BundleUploadInBase,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await create_build(db, data)
    return data


@router.post("/build/" + BuildType.BUNDLE_URL.value, tags=["tool"])
async def api_create_buundle_url(
    data:  BundleUrlInReq,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await create_build(db, data)
    return data


@router.post("/build/" + BuildType.DOCKERFILE.value, tags=["tool"])
async def api_create_dockerfile(
    data:  DockerfileUrlInReq,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await create_build(db, data)
    return data


@router.post("/build/" + BuildType.BUNDLE_GIT.value, tags=["tool"])
async def api_create_git(
    data:  GitrlInReq,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await create_build(db, data)
    return data


@router.post("/build/" + BuildType.REGISTRY_PRIVATE.value, tags=["tool"])
async def api_create_private_registry(
    data:  DockerPrivaterlInReq,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await create_build(db, data)
    return data


@router.post("/build/" + BuildType.REGISTRY_PUBLIC.value, tags=["tool"])
async def api_create_public_registry(
    data:  DockerPublicrlInReq,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await create_build(db, data)
    return data


# Edit Builds


# api_edit_public_registry
@router.put("/build/" + BuildType.BUNDLE_UPLOAD.value + "/{build_id}", tags=["tool"])
async def api_edit_bundle_upload(
    data:  BundleUploadInBase,
    build_id: str,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await edit_build(db,  build_id,  data)
    return data


@router.put("/build/" + BuildType.BUNDLE_URL.value + "/{build_id}", tags=["tool"])
async def api_edit_buundle_url(
    data:  BundleUrlInReq,
    build_id: str,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await edit_build(db,  build_id,  data)
    return data


@router.put("/build/" + BuildType.DOCKERFILE.value + "/{build_id}", tags=["tool"])
async def api_edit_dockerfile(
    data:  DockerfileUrlInReq,
    build_id: str,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await edit_build(db,  build_id,  data)
    return data


@router.put("/build/" + BuildType.BUNDLE_GIT.value + "/{build_id}", tags=["tool"])
async def api_edit_git(
    data:  GitrlInReq,
    build_id: str,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await edit_build(db,  build_id,  data)
    return data


@router.put("/build/" + BuildType.REGISTRY_PRIVATE.value + "/{build_id}", tags=["tool"])
async def api_edit_private_registry(
    data:  DockerPrivaterlInReq,
    build_id: str,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await edit_build(db,  build_id,  data)
    return data


@router.put("/build/" + BuildType.REGISTRY_PUBLIC.value + "/{build_id}", tags=["tool"])
async def api_edit_public_registry(
    data:  DockerPublicrlInReq,
    build_id: str,
    db: AsyncIOMotorClient = Depends(get_database),

):
    data = await edit_build(db,  build_id,  data)
    return data
