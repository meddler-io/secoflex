from app.models.tool.integrated.docker_build import DockerImageSpec
from app.models.tool.executor import ExecutionStatus
from app.crud.builds import get_build_executor, set_build_executor_status
import logging
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Header, Request

from ....db.mongodb import AsyncIOMotorClient, get_database

router = APIRouter()


@router.get("/result/failure/{id}",
            tags=["result"]
            )
async def api_get_build_executor(
        id: str,
        # data=Body(...,),
        db: AsyncIOMotorClient = Depends(get_database),
):

    result = await get_build_executor(db, id)
    # result = await set_build_executor_status(db, id, ExecutionStatus.INITIATED)

    return result


@router.post("/result/failure/{id}",
             tags=["result"]
             )
async def api_result_on_failure(
        id: str,
        request: Request,
        status: Optional[str] = Header("d_status"),
        message: Optional[str] = Header("d_msg"),
        # data=Body(...,),
        db: AsyncIOMotorClient = Depends(get_database),
):

    result = await set_build_executor_status(db, id, ExecutionStatus.FAILURE)
    req_body = await request.body()
    print('req_body', req_body)
    return result


@router.post("/result/success/{id}",
             tags=["result"]
             )
async def api_result_on_success(
        id: str,
        result:  DockerImageSpec = Body(...),
        status: Optional[str] = Header("default_status"),
        message: Optional[str] = Header("default_message"),
        db: AsyncIOMotorClient = Depends(get_database),
):

        print(result)
        result = await set_build_executor_status(db, id, ExecutionStatus.SUCCESS, result)
        return result
