
import asyncio
from time import sleep
import aio_pika
import logging
from aio_pika import connect, Message, DeliveryMode, ExchangeType


Connection = None

RABBITMQ_HOST = "192.168.29.5"

class Rmq:

    async def InitLoop(self, loop: asyncio.AbstractEventLoop):
        while True:
            try:
                self.Connection = await aio_pika.robust_connection.connect_robust(
                    "amqp://user:bitnami@"  + RABBITMQ_HOST,
                    # loop=loop
                )
                logging.info("Connected to rmq")

                break
            except Exception as err:
                logging.info("Failed to establish connection with RMQ")
                logging.info("Retring in 2 sec")
                self.Connection = None
                await asyncio.sleep(2)

    async def Init(self):

        while True:
            try:
                self.Connection = await aio_pika.robust_connection.connect_robust(
                    "amqp://user:bitnami@"  + RABBITMQ_HOST,

                )
                logging.info("Connected to rmq")

                break
            except:
                logging.info("Failed to establish connection with RMQ")
                logging.info("Retring in 2 sec")
                self.Connection = None
                sleep(2)

        # self.Connection.add_close_callback( self.on_close )

    async def publish(self, topic: str,  data: str):

        if self.Connection == None:
            logging.info("Rmq not initiated")
            return False

        if self.Connection.reconnecting:
            logging.info("Rmq is dead")

            raise Exception("Rmq is dead")
        routing_key = topic
        logging.info("Writting to MQ")
        channel = await self.Connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body="{}".format(data).encode()),
            routing_key=routing_key,
            timeout=4

        )
        return True


RMQ = Rmq()
