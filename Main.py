# TODO Instead of "condencing" things into a ticker to rep a bond allo, maybe create some sort of umbrella function
# TODO make it so if the target allocations have a ticker not in portfolio yet it properly displays in compare
from Formatting import stringify_dollar, stringify_percentage
from Transactions import Transaction, Transactions
from Portfolio import Position
import Build_Dictionaries, math
BOND_TICKERS = ['SCHZ']

portfolio = Build_Dictionaries.retrieve_portfolio()
portfolio.condence_position(['BND'], BOND_TICKERS)
allocations_dict = Build_Dictionaries.retrieve_allocations()

base_allocation_amount = round(portfolio.positions['CASH'].in_dollars() - (allocations_dict['CASH']*portfolio.total), 2)
transaction_list = Transactions({}, base_allocation_amount, portfolio.total)

# Returns ticker, or nothing if ticker not found in portfolio / allocations
def input_ticker(text_str):
    allocation_ticker = ""
    try: 
        allocation_ticker = input("\n"+text_str).upper()
        allocations_dict[allocation_ticker]
        portfolio.percentage_held(allocation_ticker)
        return allocation_ticker
    except KeyError:
        print("Could not find ticker in portfolio / allocations")
        print("")
        return ""

# Helper function for printing an allocation
def print_allocation_differences(dollar_allo, percentage_allo, shares):
    print("\n%-15s %-15s %-15s" %("AMNT_$$", "PERCENTAGE", "SHARES"))
    print("%-15s %-15s %-15s\n" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))

while True:
    command = input("Enter command: ")
    match command.lower():
        case 'exit':
            with open('supporting_files/dump.txt', 'w') as f:
                f.writelines(transaction_list.__str__())
            break

        case 'compare':
            print("\n%-10s %15s %15s %15s %15s %15s" %("TICKER", "DOLLAR_AMNT","SHARE_PRICE",  "CURRENT", "TARGET", "SHORTFALL"))
            for key in portfolio.positions:
                percentage_held = stringify_percentage(portfolio.percentage_held(key))
                dollar_amount =  stringify_dollar(portfolio.positions[key].in_dollars())
                shortfall = stringify_percentage(allocations_dict[key]-portfolio.percentage_held(key))
                share_price = stringify_dollar(portfolio.positions[key].share_price)
                target_allocation = stringify_percentage(allocations_dict[key])
                print("%-10s %15s %15s %15s %15s %15s" %(key, dollar_amount, share_price, percentage_held, target_allocation, shortfall))
            
        case 'allocate':
            allocation_ticker = input_ticker("Enter ticker: ")
            if allocation_ticker == "":
                continue
            shortfall = allocations_dict[allocation_ticker]-portfolio.percentage_held(allocation_ticker)
            percentage_allo = shortfall
            dollar_allo = shortfall*portfolio.total
            share_price = portfolio.positions[allocation_ticker].share_price
            shares = dollar_allo/share_price
            print_allocation_differences(dollar_allo, percentage_allo, shares)
            if shortfall < 0:
                print("\nmust be under allocated to submit allocation")
            else:
                if dollar_allo > transaction_list.current_allocation_ammount:
                    print("\nFull allocation requires more than amount to allocate. Will only allocate up to amount can.  New values")
                    dollar_allo = transaction_list.current_allocation_ammount
                    percentage_allo = dollar_allo/portfolio.total
                    shares = dollar_allo/share_price
                    print_allocation_differences(dollar_allo, percentage_allo, shares)
                shares = float(input("How many shares should be purchased? "))
                dollar_allo = share_price * shares
                percentage_allo = dollar_allo/portfolio.total
                print("New values")
                print_allocation_differences(dollar_allo, percentage_allo, shares)
                confirm = input("\nconfirm allocation (y/n)? ")
                if confirm.lower() == "y":
                    try:
                        transaction_list.add_transaction(allocation_ticker, Transaction(shares, dollar_allo))
                    except KeyError:
                        print("Transaction for ticker exists, use upd_trn")

        case 'auto_allo':
            dict_shortfall = {}
            for key in portfolio.positions:
                shortfall = allocations_dict[key]-portfolio.percentage_held(key)
                dict_shortfall[key] = shortfall
            sorted_dict = sorted(dict_shortfall.items(), key=lambda x:x[1], reverse=True)
            arr_allos = []
            for ticker in sorted_dict:
                if(ticker[1] > 0):
                    arr_allos.append(ticker)
            for ticker in arr_allos:
                allocation_ticker = ticker[0]
                shortfall = ticker[1]
                share_price = portfolio.positions[allocation_ticker].share_price
                shares = math.floor((shortfall*portfolio.total)/share_price)
                dollar_allo = share_price * shares
                if shares == 0:
                    shares = 1
                    dollar_allo = share_price * shares
                if dollar_allo > transaction_list.current_allocation_ammount:
                    shares = math.floor((transaction_list.current_allocation_ammount)/share_price)
                    dollar_allo = share_price * shares
                if shares != 0:
                    transaction_list.add_transaction(allocation_ticker, Transaction(shares, dollar_allo))
            print(transaction_list.__str__())

            # make function for accepting changes?
            # make so works mid working through (will error if trn added before I think)?
        case 'auto_sell':
            dict_shortfall = {}
            for key in portfolio.positions:
                if(key != "CASH"):
                    shortfall = allocations_dict[key]-portfolio.percentage_held(key)
                    dict_shortfall[key] = shortfall
            sorted_dict = sorted(dict_shortfall.items(), key=lambda x:x[1], reverse=False)
            arr_allos = []
            for ticker in sorted_dict:
                if(ticker[1] < 0):
                    arr_allos.append(ticker)
            for ticker in arr_allos:
                allocation_ticker = ticker[0]
                over_allocation = ticker[1]
                share_price = portfolio.positions[allocation_ticker].share_price
                shares = math.floor(over_allocation*portfolio.total/share_price*-1)
                dollar_allo = shares*share_price*-1
                if(shares != 0):
                    transaction_list.add_transaction(allocation_ticker, Transaction(shares, (dollar_allo)))
                
            print(transaction_list.__str__())
        
        case 'compare_trn':
            print("\n%-10s %15s %15s %15s %15s" %("TICKER", "DOLLAR_AMNT", "TARGET", "SHORTFALL_BFR", "SHORTFALL_AFTR"))
            for key in portfolio.positions:
                dollar_amount =  stringify_dollar(portfolio.positions[key].in_dollars())
                target_allocation = stringify_percentage(allocations_dict[key])
                shortfall_bfr = stringify_percentage(allocations_dict[key]-portfolio.percentage_held(key))
                allocations_dict[key]-portfolio.percentage_held(key)
                shortfall_aftr = ""
                try:
                    per_trn =  transaction_list.transactions[key].cost/transaction_list.portfolio_total
                    shortfall_aftr = stringify_percentage(allocations_dict[key]-(portfolio.percentage_held(key)+per_trn))
                except:
                    shortfall_aftr = shortfall_bfr 
                print("%-10s %15s %15s %15s %15s" %(key, dollar_amount, target_allocation, shortfall_bfr, shortfall_aftr))
            
        case 'sell':
            allocation_ticker = input_ticker("Enter ticker: ")
            if allocation_ticker == "":
                continue
            over_allocation = portfolio.percentage_held(allocation_ticker) - allocations_dict[allocation_ticker]
            percentage_allo = over_allocation
            dollar_allo = over_allocation*portfolio.total
            share_price = portfolio.positions[allocation_ticker].share_price
            shares = dollar_allo/share_price
            print_allocation_differences(dollar_allo, percentage_allo, shares)
            shares = float(input("How many shares should be sold? "))
            dollar_allo = share_price * shares
            percentage_allo = dollar_allo/portfolio.total
            print_allocation_differences(dollar_allo, percentage_allo, shares)
            confirm = input("\nconfirm allocation (y/n)? ")
            if confirm.lower() == "y":
                try:
                    transaction_list.add_transaction(allocation_ticker, Transaction(shares, (-1*dollar_allo)))
                except KeyError:
                    print("Transaction for ticker exists, use upd_trn")

        case 'reset':
            transaction_list.reset()

        case 'trans':
            print(transaction_list.__str__())

        case 'new_ticker':
            ticker = input("Enter ticker: ").upper()
            share_price = input("Share price: ")
            portfolio.add_position(ticker, Position(0.00 ,share_price))
            allocations_dict[ticker] = 0.00

        case 'upd_money':
            amount = float(input("Amount to add: "))
            portfolio.update_position('CASH', Position(amount, 1.0))
            base_allocation_amount = round(portfolio.positions['CASH'].in_dollars() - (allocations_dict['CASH']*portfolio.total), 2)
            transaction_list = Transactions({}, base_allocation_amount, portfolio.total)

        case 'rmv_trn':
            ticker = input_ticker("Enter ticker to remove: ")
            if ticker == "":
                continue
            transaction_list.rmv_transaction(ticker)
        
        case 'upd_trn':
            ticker = input_ticker("Enter ticker to update: ")
            if ticker == "":
                continue
            shares = float(input("Enter number of shares: "))
            cost = portfolio.positions[ticker].share_price * shares
            transaction_list.upd_transaction(ticker, Transaction(shares, cost))

        case 'help':
            with open('help.txt', newline='') as file:
                iterator = 1
                command = ""
                for line in file.readlines():
                    if iterator % 2 == 0:
                        command = line.strip()
                    else:
                        print("%-15s %-20s" %(command, line.strip()))
                    iterator = iterator + 1
        case _:
            print("Command not found")

    print("")
