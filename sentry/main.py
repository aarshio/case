from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from ib_insync import *
import nest_asyncio

nest_asyncio.apply()
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

async def job():
    print(ib.reqAllOpenOrders())

scheduler = AsyncIOScheduler()
scheduler.add_job(job, "interval", seconds=1)

scheduler.start()

asyncio.get_event_loop().run_forever()