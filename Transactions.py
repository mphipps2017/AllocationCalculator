# TODO make into it's own class. Swap to just using transaction and keep dict in main class

from Formatting import stringify_dollar, stringify_percentage

class Transaction:
    def __init__(self, shares, cost):
        self.shares = shares
        self.cost = cost


def print_to_file(prefix, transaction_list, portfolio_total):
    with open('dump.txt', 'w') as f:
        f.writelines(prefix + print_transactions(transaction_list, portfolio_total))

def print_transactions(transaction_list, portfolio_total):
    ret_str = "Allocations" + "\n%-10s %15s %15s %15s" %("TICKER", "SHARES",  "DOLLAR", "PERCENTAGE")
    total_dollar = 0.0
    total_percentage = 0.0
    for key in transaction_list:
        dollar_amt = stringify_dollar(transaction_list[key].cost)
        shares = transaction_list[key].shares
        percentage_amt_float = transaction_list[key].cost/portfolio_total
        percentage_amt = stringify_percentage(percentage_amt_float)
        total_dollar = total_dollar + transaction_list[key].cost
        total_percentage = total_percentage + percentage_amt_float
        ret_str = ret_str + "\n%-10s %15s %15s %15s" %(key,  shares, dollar_amt, percentage_amt)
    return ret_str + "\n%-10s %15s %15s %15s" %("TOTALS",  "", stringify_dollar(total_dollar), stringify_percentage(total_percentage))
    