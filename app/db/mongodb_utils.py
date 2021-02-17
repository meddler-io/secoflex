import logging
from engine.integrations import rmq
from engine.integrations.minio import  init as init_minio
from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .mongodb import db
import asyncio


async def connect_to_mongo():
    logging.info("Connecting to Mongos")
    logging.info( MONGODB_URL)

    db.client = AsyncIOMotorClient(str(MONGODB_URL),
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    logging.info("Connectied to Mongo")
    logging.info("Connecting to Rmq")

    # Rmq Pika Loop
    # current_loop = asyncio.get_event_loop()
    # new_loop = asyncio.new_event_loop()
    # init_minio()
    asyncio.create_task(rmq.RMQ.InitLoop(loop=None))



async def close_mongo_connection():
    logging.info("Closing Mongo")
    db.client.close()
    logging.info("Closed Mongo")
