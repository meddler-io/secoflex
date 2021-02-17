from app.models.tool.build.bundle_upload import BundleUploadInBase
import asyncio
import json
from logging import log
from pathlib import PurePath
from ....core.config import FAILURE_EXECUTION_WEBHOOK, FILESTORAGE_PATH, SUCCESS_EXECUTION_WEBHOOK
from typing import Any, Dict, Optional, List
from ....core.utils import save_upload_file
from fastapi import APIRouter, Body, Depends, HTTPException
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.tool.builds import BundleGitInReq, RegistryPrivateInReq, RegistryPrivateInResp
from ....models.tool.builds import BuildMessageSpec
from ....models.tool.builds import RegistryPublicInReq, RegistryPublicInResp
from ....crud.builds import create_build, create_build_executor, get_all_build, get_all_build_executor, get_build, update_build_config, get_build_config
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
# Create an Build

# Reg. Public


@router.post("/build/" + BuildType.REGISTRY_PUBLIC.value,
             response_model=RegistryPublicInResp,
             tags=["build"]
             )
async def api_create_public_registry(
        db: AsyncIOMotorClient = Depends(get_database),
    build: RegistryPublicInReq = Body(...,),
):

    response = await create_build(db, BuildType.REGISTRY_PUBLIC, build)
    return response


@router.get("/build/{tool_id}",
            #  response_model=Any],
            tags=["build"]
            )
async def api_get_all_public_registry(
        tool_id: str,
        db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_all_build(db, tool_id)
    return response


# Reg. Private
@router.post("/build/" + BuildType.REGISTRY_PRIVATE.value,
             response_model=RegistryPrivateInResp,
             tags=["build"]
             )
async def api_create_private_registry(
        db: AsyncIOMotorClient = Depends(get_database),
    build: RegistryPrivateInReq = Body(...,),
):

    response = await create_build(db, BuildType.REGISTRY_PRIVATE, build)
    return response


@router.post("/build/run/{id}", tags=["tool"])
async def api_run_build(
    id: str,
    db: AsyncIOMotorClient = Depends(get_database),
):
    try:
        result = await get_build(db,  id)
        if result.type == BuildType.REGISTRY_PUBLIC:
            pass
        elif result.type == BuildType.REGISTRY_PRIVATE:
            pass
        elif result.type == BuildType.BUNDLE_GIT:
            pass
        elif result.type == BuildType.BUNDLE_UPLOAD:
            pass
        elif result.type == BuildType.BUNDLE_URL:
            pass
        else:
            pass

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
        return False

    return True


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
        print(err)
        return False

    return True


@router.get("/build/executors/{id}", tags=["tool"])
async def api_get_all_build_executor(
    id: str,
    db: AsyncIOMotorClient = Depends(get_database),
):
    response = await get_all_build_executor(db, id)
    return response


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

@router.post("/build/new/" + BuildType.BUNDLE_UPLOAD.value, tags=["tool"])
async def api_test_0(
    data:  BundleUploadInBase,
):

    return data


@router.post("/build/new/" + BuildType.BUNDLE_URL.value, tags=["tool"])
async def api_test_1(
    data:  BundleUrlInReq,
):

    return data


@router.post("/build/new/" + BuildType.DOCKERFILE.value, tags=["tool"])
async def api_test_2(
    data:  DockerfileUrlInReq,
):

    return data

@router.post("/build/new/" + BuildType.BUNDLE_GIT.value, tags=["tool"])
async def api_test_3(
    data:  GitrlInReq,
):

    return data

@router.post("/build/new/" + BuildType.REGISTRY_PRIVATE.value, tags=["tool"])
async def api_test_4(
    data:  DockerPrivaterlInReq,
):

    return data


@router.post("/build/new/" + BuildType.REGISTRY_PUBLIC.value, tags=["tool"])
async def api_test_5(
    data:  DockerPublicrlInReq,
):

    return data

