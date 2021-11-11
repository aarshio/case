from datetime import datetime
from ib_insync import Option, Stock

def save_open_positions(*args):
    try:
        print('Saving open positions...')
        ib = args[0]
        db = args[1]

        stocks = dict()
        options = dict()

        positions = ib.positions()

        for position in positions:
            contract = position.contract
            common = ['position', 'avgCost']
            if isinstance(contract, Stock):
                other = ['exchange', 'currency', 'localSymbol']
                temp = {}
                for include in common:
                    temp[include] = getattr(position, include)
                for include in other:
                    temp[include] = getattr(contract, include)
                stocks[contract.symbol] = temp
            elif isinstance(contract, Option):
                other = ['lastTradeDateOrContractMonth', 'strike', 'right', 'currency', 'localSymbol']
                temp = {}
                for include in common:
                    temp[include] = getattr(position, include)
                for include in other:
                    temp[include] = getattr(contract, include)
                options[contract.symbol] = temp
        
        result=db.positions.insert_one({'case_timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f%z"), 'options': options, 'stocks': stocks})
        print("Success! Open positions saved", result)
    except Exception as e:
        print("Error saving open positions:", e)