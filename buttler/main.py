from datetime import datetime
import os
from os.path import join, dirname
import csv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from dotenv import load_dotenv
import nest_asyncio
from pymongo import MongoClient

nest_asyncio.apply()
scheduler = AsyncIOScheduler()

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

MONGO_URI = os.environ.get("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    universe = client.universe
    print("[B] DB connected")
except:
    print("[B] Failed to connect to db")


async def startup():
    try:
        print("[B] Running universe sync...")
        with open('./buttler/quotes.csv') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[0] != 'Symbol':
                    key = {"_id": row[0]}
                    universe.all.update_one(
                        key, {'$setOnInsert': {'symbol': row[0]}}, upsert=True)
        universe.fresh.update_one({"_id": "all"}, {"$set": {"last_run": datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%S.%f%z")}}, upsert=True)
        print(f'[B] Success! Updated symbols')
    except Exception as e:
        print(e)
        pass

asyncio.run(startup())

# scheduler.add_job(job, "interval", seconds=3)
# scheduler.add_job(job2, "interval", seconds=1)

scheduler.start()

asyncio.get_event_loop().run_forever()
