from jobs.positions import savePositions
from env import MONGO_URI

import asyncio
import nest_asyncio
from ib_insync import IB
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler

nest_asyncio.apply()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=0)

client = MongoClient(MONGO_URI)
db = client.kipp

scheduler = AsyncIOScheduler()
scheduler.add_job(savePositions, "interval", [ib, db], seconds=15)

scheduler.start()

asyncio.get_event_loop().run_forever()