import asyncio
import aio_pika
import logging
from engine.integrations import produce_data
from engine import integrations
from fastapi import APIRouter
from typing import Dict
import json
from engine.integrations import rmq
router = APIRouter()

# Test
# Test endpoint


@router.get("/test", tags=["test"])
async def api_test(
    data:  Dict[str, str]
):
    try:
        await asyncio.wait_for(rmq.RMQ.publish(json.dumps(data)), timeout=4)
    except:
        return False


    return True
