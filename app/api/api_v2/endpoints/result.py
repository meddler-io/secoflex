from app.models.tool.executor import ExecutionStatus
from app.crud.builds import get_build_executor, set_build_executor_status
import logging
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Header

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
        status: Optional[str] = Header("d_status"),
        message: Optional[str] = Header("d_msg"),
        # data=Body(...,),
        db: AsyncIOMotorClient = Depends(get_database),
):

    result = await set_build_executor_status(db, id, ExecutionStatus.FAILURE)
    return result


@router.post("/result/success/{id}",
             tags=["result"]
             )
async def api_result_on_success(
        id: str,
        status: Optional[str] = Header("default_status"),
        message: Optional[str] = Header("default_message"),
        db: AsyncIOMotorClient = Depends(get_database),
):


    result = await set_build_executor_status(db, id, ExecutionStatus.SUCCESS)
    return result