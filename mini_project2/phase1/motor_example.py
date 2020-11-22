import pymongo
import motor.motor_asyncio
import asyncio

import pprint

db = motor.motor_asyncio.AsyncIOMotorClient()['291db']

async def do_find_one():
    document = await db['posts'].find_one()
    pprint.pprint(document)

loop = asyncio.get_event_loop()
loop.run_until_complete(do_find_one())


