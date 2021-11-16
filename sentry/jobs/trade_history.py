from datetime import datetime
from datetime import datetime
from env import FLEX_QUERY_TOKEN, FLEX_QUERY_ID
from ib_insync import FlexReport

async def save_trade_history(*args):
    try:
        db = args[0]
        print('Running trade history job...')
        statement = FlexReport(token=FLEX_QUERY_TOKEN, queryId=FLEX_QUERY_ID, path=None)
        trades = statement.extract('Trade', parseNumbers=True)
        for trade in trades:
            data = vars(trade)
            key = {"_id": data['tradeID']}
            db.history.update(key, data, upsert=True)
        db.fresh.update({"_id": "history"}, {"last_run":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f%z")}, upsert=True)
        print(f'Success! Updated {len(trades)} trades')
    except Exception as e:
        print(e)
        pass