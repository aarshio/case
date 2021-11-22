import os
from os.path import join, dirname
from datetime import datetime
from jobs.positions import save_open_positions
from jobs.trade_history import save_trade_history

import asyncio
from dotenv import load_dotenv
import nest_asyncio
from ib_insync import IB
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler

nest_asyncio.apply()


dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

MONGO_URI = os.environ.get("MONGO_URI")
FLEX_QUERY_TOKEN = os.environ.get("FLEX_QUERY_TOKEN")
FLEX_QUERY_ID = os.environ.get("FLEX_QUERY_ID")

ib = IB()
scheduler = AsyncIOScheduler()

try:
    client = MongoClient(MONGO_URI)
    db = client.kipp
    db_trades = client.trades
    print("[S] DB connected")
except:
    print("[S] Failed to connect to db")

scheduler.add_job(save_trade_history, "interval", [
                  db_trades, FLEX_QUERY_TOKEN, FLEX_QUERY_ID], next_run_time=datetime.now(), hours=4, max_instances=1)

# jobs that require ib connection

try:
    ib.connect('127.0.0.1', 7496, clientId=0)
except:
    print("[S] TWS port not found")


if ib.isConnected():
    print("[S] IB active")

    # recurring jobs
    scheduler.add_job(save_open_positions, "interval", [ib, db], seconds=15)
else:
    print("[S] IB inactive")

scheduler.start()

asyncio.get_event_loop().run_forever()
