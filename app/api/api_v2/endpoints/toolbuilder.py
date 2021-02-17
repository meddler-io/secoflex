from pathlib import PurePath
from ....core.config import FILESTORAGE_PATH
from typing import Any, Optional, List
from ....core.utils import save_upload_file
from fastapi import APIRouter, Body, Depends, HTTPException
from ....db.mongodb import AsyncIOMotorClient, get_database
from starlette.responses import FileResponse
from ....models.tool.tool import ToolInReq, ToolInResp
from ....crud.toolbuilder import run_toolbuilder
from typing import Dict
from engine.integrations import rmq
import asyncio
import json


router = APIRouter()

# Toolbuilder: Zip/Tar
# Create an toolbuilder
# Private Tool: Check for insecure input data points
@router.post("/toolbuilder/zip", tags=["toolbuilder"])
async def api_run_toolbuilder(
    data:  Any = Body(...),
    tool: ToolInReq = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),

):
    try:
        await run_toolbuilder(db , tool)
        await asyncio.wait_for(rmq.RMQ.publish(json.dumps(data)), timeout=4)
    except:
        return False

    return True


# Toolbuilder
# Create an toolbuilder
@router.post("/toolbuilder/image", tags=["toolbuilder"])
async def api_run_toolbuilder(
    data:  Any = Body(...),
    tool: ToolInReq = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),

):
    try:
        await run_toolbuilder(db , tool)
        await asyncio.wait_for(rmq.RMQ.publish( "tasks_test",  json.dumps(data)), timeout=4)
    except:
        return False

    return True



# Toolbuilder
# Create an toolbuilder
@router.post("/toolbuilder/git", tags=["toolbuilder"])
async def api_run_toolbuilder(
    data:  Any = Body(...),
    tool: ToolInReq = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),

):
    try:
        await run_toolbuilder(db , tool)
        await asyncio.wait_for(rmq.RMQ.publish(json.dumps(data)), timeout=4)
    except:
        return False

    return True

# Toolbuilder
# Create an toolbuilder
@router.post("/toolbuilder/dockerfile", tags=["toolbuilder"])
async def api_run_toolbuilder(
    data:  Any = Body(...),
    tool: ToolInReq = Body(...,),
    db: AsyncIOMotorClient = Depends(get_database),

):
    try:
        await run_toolbuilder(db , tool)
        await asyncio.wait_for(rmq.RMQ.publish(json.dumps(data)), timeout=4)
    except:
        return False

    return True

