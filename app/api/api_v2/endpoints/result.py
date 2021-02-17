import logging
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Header

from ....db.mongodb import AsyncIOMotorClient, get_database

router = APIRouter()



@router.post("/result/failure/{id}",
             tags=["result"]
             )
async def api_cresult_on_failure(
        id: str,
        status: Optional[str] = Header( "d_status"),
        message: Optional[str] = Header("d_msg"),
        # data=Body(...,),
        db: AsyncIOMotorClient = Depends(get_database),
):

    print("status"+status)
    print("message"+ message)
#     logging.log("WebHook", id,  data)
    print("failure")

    return ""


@router.post("/result/success/{id}",
             tags=["result"]
             )
async def api_cresult_on_success(
        id: str,
        status: Optional[str] = Header("default_status"),
        message: Optional[str] = Header("default_message"),
        db: AsyncIOMotorClient = Depends(get_database),
        data=Body(...,),
):

    print("status", status)
    print("message", message)
    # logging.log("WebHook", id,  data)
    print("success")

    return ""
