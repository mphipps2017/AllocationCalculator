from Formatting import stringify_dollar, stringify_percentage

class Transaction:
    def __init__(self, shares, cost):
        self.shares = shares
        self.cost = cost

class Transactions:
    def __init__(self, transactions, allocation_amount, portfolio_total):
        self.base_allocation_amount = allocation_amount
        self.current_allocation_ammount = allocation_amount
        self.transactions = transactions
        self.portfolio_total = portfolio_total
    
    def __str__(self):
        total = self.portfolio_total
        base = self.base_allocation_amount
        current = self.current_allocation_ammount
        ret_str = "Base allocation"
        ret_str = ret_str + "\nDollars: " + stringify_dollar(base)
        ret_str = ret_str + "\nPercentage: " + stringify_percentage(base/total)
        ret_str = ret_str + "\n\nCurrent allocation"
        ret_str = ret_str + "\nDollars: " + stringify_dollar(current)
        ret_str = ret_str + "\nPercentage: " + stringify_percentage(current/total)
        ret_str = ret_str + "\n\nAllocations" + "\n%-10s %15s %15s %15s" %("TICKER", "SHARES",  "DOLLAR", "PERCENTAGE")
        total_dollar = 0.0
        total_percentage = 0.0
        transaction_list = self.transactions
        for key in transaction_list:
            dollar_amt = stringify_dollar(transaction_list[key].cost)
            shares = transaction_list[key].shares
            percentage_amt_float = transaction_list[key].cost/total
            percentage_amt = stringify_percentage(percentage_amt_float)
            total_dollar = total_dollar + transaction_list[key].cost
            total_percentage = total_percentage + percentage_amt_float
            ret_str = ret_str + "\n%-10s %15s %15s %15s" %(key,  shares, dollar_amt, percentage_amt)
        return ret_str + "\n%-10s %15s %15s %15s" %("TOTALS",  "", stringify_dollar(total_dollar), stringify_percentage(total_percentage))
    
    def add_transaction(self, ticker, transaction):
        try: 
            self.transactions[ticker]
            raise Exception("Ticker already exists in transaction list, use update")
        except KeyError:
            self.current_allocation_ammount = self.current_allocation_ammount - transaction.cost
            self.transactions[ticker] = transaction

    def rmv_transaction(self, ticker):
        self.current_allocation_ammount = self.current_allocation_ammount + self.transactions[ticker].cost
        return self.positions.pop(ticker)

    def upd_transaction(self, ticker, transaction):
        self.current_allocation_ammount = self.current_allocation_ammount - transaction.cost + self.transactions[ticker].cost
        self.transactions[ticker] = transaction

    def reset(self):
        self.current_allocation_ammount = self.base_allocation_amount
        self.transactions = {}