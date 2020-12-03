from pathlib import PurePath
from ....core.config import FILESTORAGE_PATH
from typing import Optional, List
from ....core.utils import save_upload_file
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import FastAPI, File, UploadFile, Query
from ....core.jwt import get_current_user_authorizer
from ....db.mongodb import AsyncIOMotorClient, get_database
from starlette.responses import FileResponse
from ....models.asset_schema import HostAssetSchema, HostAssetSchemaResponse, DomainAssetSchema, DomainAssetSchemaResponse, WebAssetSchema, WebAssetSchemaResponse, AndroidAssetSchema, AndroidAssetSchemaResponse, IosAssetSchema, IosdAssetSchemaResponse, RepositoryAssetSchema, RepositoryAssetSchemaResponse, DockerAssetSchema, DockerAssetSchemaResponse
from ....crud.asset_host_schema import create_host_asset, get_host_asset, get_all_host_asset
from ....crud.asset_domain_schema import create_domain_asset, get_all_domain_asset
from ....crud.asset_web_schema import create_web_asset, get_all_web_asset, get_web_asset
from ....crud.asset_android_schema import create_android_asset, get_all_android_asset, get_android_asset
from ....crud.asset_ios_schema import create_ios_asset, get_all_ios_asset, get_ios_asset
from ....crud.asset_repository_schema import create_repository_asset, get_all_repository_asset, get_repository_asset
from ....crud.asset_docker_schema import create_docker_asset, get_all_docker_asset, get_docker_asset

router = APIRouter()

# Host
# Create an asset


@router.post("/asset/host", response_model=HostAssetSchemaResponse, tags=["asset"])
async def create_asset_host_api(
    hostAssetSchema: HostAssetSchema = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),
):

    # hostAssetSchema.create_form_id()
    file_in_response = await create_host_asset(db, hostAssetSchema)
    return file_in_response


# Create an asset
@router.get("/asset/host", tags=["asset"])
async def get_asset_host_api(
    db: AsyncIOMotorClient = Depends(get_database),
):

    # hostAssetSchema.create_form_id()
    file_in_response = await get_all_host_asset(db)
    return file_in_response


# Domain
# Create an Domain
@router.post("/asset/domain", response_model=DomainAssetSchemaResponse, tags=["asset"])
async def create_asset_domain_api(
    asset: DomainAssetSchema = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),
):

    # hostAssetSchema.create_form_id()
    response = await create_domain_asset(db, asset)
    return response


# Create an Domain
@router.get("/asset/domain", tags=["asset"])
async def get_asset_domain_api(
    db: AsyncIOMotorClient = Depends(get_database),
):

    # hostAssetSchema.create_form_id()
    response = await get_all_domain_asset(db)
    return response


# WEB
# Create an Web
@router.post("/asset/web", response_model=WebAssetSchemaResponse, tags=["asset"])
async def create_asset_web_api(
    asset: WebAssetSchema = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),
):
    # hostAssetSchema.create_form_id()
    response = await create_web_asset(db, asset)
    return response


# Create an Web
@router.get("/asset/web", tags=["asset"])
async def get_asset_web_api(
    db: AsyncIOMotorClient = Depends(get_database),
):

    # hostAssetSchema.create_form_id()
    response = await get_all_web_asset(db)
    return response


# Android
# Create an Android
@router.post("/asset/android", response_model=AndroidAssetSchemaResponse, tags=["asset"])
async def create_asset_android_api(
    asset: AndroidAssetSchema = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),
):
    response = await create_android_asset(db, asset)
    return responsemo


# Create an Android
@router.get("/asset/android", tags=["asset"])
async def get_asset_android_api(
    db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_all_android_asset(db)
    return response


# IOS
# Create an IOS
@router.post("/asset/ios", response_model=IosdAssetSchemaResponse, tags=["asset"])
async def create_asset_ios_api(
    asset: IosAssetSchema = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),
):
    response = await create_ios_asset(db, asset)
    return response


# Create an IOS
@router.get("/asset/ios", tags=["asset"])
async def get_asset_ios_api(
    db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_all_ios_asset(db)
    return response


# Repository
# Create an Repository
@router.post("/asset/repository", response_model=RepositoryAssetSchemaResponse, tags=["repository"])
async def create_asset_repository_api(
    asset: RepositoryAssetSchema = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),
):
    response = await create_repository_asset(db, asset)
    return response


# Create an Repository
@router.get("/asset/repository", tags=["repository"])
async def get_asset_repository_api(
    db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_all_repository_asset(db)
    return response


# Docker
# Create an Docker
@router.post("/asset/docker", response_model=DockerAssetSchemaResponse, tags=["docker"])
async def create_asset_docker_api(
    asset: DockerAssetSchema = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),
):
    response = await create_docker_asset(db, asset)
    return response


# Create an Docker
@router.get("/asset/docker", tags=["docker"])
async def get_asset_docker_api(
    db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_all_docker_asset(db)
    return response
