from pathlib import PurePath
from ....core.config import FILESTORAGE_PATH
from typing import Any, Optional, List
from ....core.utils import save_upload_file
from fastapi import APIRouter, Body, Depends, HTTPException
from ....db.mongodb import AsyncIOMotorClient, get_database
from starlette.responses import FileResponse
from ....models.tool.tool import ToolInReq, ToolInResp, ToolModifyInReq
from ....crud.tools import edit_tool, get_tool, get_tools, create_tool

from typing import Dict
from engine.integrations import rmq
import asyncio
import json


router = APIRouter()

# Tool
# Create an Tool


@router.post("/tool", tags=["tool"],
             response_model=ToolInResp

             )
async def api_create_tool(
        db: AsyncIOMotorClient = Depends(get_database),
        tool: ToolInReq = Body(...,),
):

    response = await create_tool(db, tool)
    return response


# Edit Tol
@router.put("/tool/{id}", tags=["tool"],
            response_model=ToolInResp

            )
async def api_edit_tool(
        id: str,
        db: AsyncIOMotorClient = Depends(get_database),
        tool: ToolModifyInReq = Body(...,),
):

    response = await edit_tool(db, id, tool)
    return response


# Get Tool
@router.get("/tool/{id}", tags=["tool"], response_model=ToolInResp)
async def api_get_tool(
        id: str,
        db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_tool(db, id)
    return response


# Get all Tool
@router.get("/tool",
            response_model=List[ToolInResp], tags=["tool"])
async def api_get_tools(
        db: AsyncIOMotorClient = Depends(get_database),
):

    response = await get_tools(db)
    return response


@router.post("/tool/run", tags=["tool"])
async def api_run_tool(
    data:  Any = Body(...,)
):
    try:
        await asyncio.wait_for(rmq.RMQ.publish(json.dumps(data)), timeout=4)
    except:
        return False

    return True


#  Image Builder Tool

@router.post("/toolbuilder/test", tags=["toolbuilder"])
async def api_run_toolbuilder(
    data:  Any = Body(...),
    db: AsyncIOMotorClient = Depends(get_database),

):
    try:
        response = await asyncio.wait_for(rmq.RMQ.publish("tasks_test",  json.dumps(data)), timeout=4)
        return response
    except:
        return False

    # return True
