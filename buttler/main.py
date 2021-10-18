from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import nest_asyncio

nest_asyncio.apply()

async def job():
    print("B")

scheduler = AsyncIOScheduler()
scheduler.add_job(job, "interval", seconds=3)
# scheduler.add_job(job2, "interval", seconds=1)

scheduler.start()

asyncio.get_event_loop().run_forever()