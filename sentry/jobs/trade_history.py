from datetime import datetime
from datetime import datetime
from env import FLEX_QUERY_TOKEN, FLEX_QUERY_ID
from ib_insync import FlexReport

async def save_trade_history(db):
    try:
        print('Running trade history job')
        statement = FlexReport(token=FLEX_QUERY_TOKEN, queryId=FLEX_QUERY_ID, path=None)
        trades = statement.extract('Trade', parseNumbers=True)
        for trade in trades:
            data = vars(trade)
            data['case_timestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            key = {"_id": data['tradeID']}
            db.history.update(key, data, upsert=True)
        print(f'Success! Updated {len(trades)} trades')
    except Exception as e:
        print(e)
        pass