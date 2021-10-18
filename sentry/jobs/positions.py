from ib_insync import Option, Stock

def savePositions(*args):
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
    
    result=db.positions.insert_one({'options': options, 'stocks': stocks})
    print(result)