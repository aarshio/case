from jobs.positions import save_open_positions
from jobs.trade_history import save_trade_history

from env import MONGO_URI

import asyncio
import nest_asyncio
from ib_insync import IB
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler

nest_asyncio.apply()

ib = IB()

try:
    client = MongoClient(MONGO_URI)
    db = client.kipp
    db_trades_histroy = client.trades
    print("[S] DB connected")
except:
    print("[S] Failed to connect to db")

asyncio.run(save_trade_history(db_trades_histroy))

# jobs that require ib connection

try:
    ib.connect('127.0.0.1', 7496, clientId=0)
except:
    print("[S] TWS port not found")

scheduler = AsyncIOScheduler()

if ib.isConnected():
    print("[S] IB active")

    # recurring jobs
    scheduler.add_job(save_open_positions, "interval", [ib, db], seconds=15)
else:
    print("[S] IB inactive")

scheduler.start()

asyncio.get_event_loop().run_forever()