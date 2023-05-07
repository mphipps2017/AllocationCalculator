# TODO Work on to string functions to clean up main class
# work on a function that works like allocate but for selling
from Formatting import stringify_dollar, stringify_percentage
from Transactions import Transaction, Transactions
from Build_Dictionaries import retrieve_portfolio, retrieve_allocations
BOND_TICKERS = ('SCHZ', 'AGG')

portfolio = retrieve_portfolio()
portfolio.condence_position(['BND'], BOND_TICKERS)
portfolio.condence_position(['AVUS', 'DFUS'], ['VTI'])
allocations_dict = retrieve_allocations()

base_allocation_amount = round(portfolio.positions['CASH'].in_dollars() - (allocations_dict['CASH']*portfolio.total), 2)
transaction_list = Transactions({}, base_allocation_amount, portfolio.total)

while True:
    command = input("Enter command: ")
    match command.lower():
        case 'exit':
            with open('dump.txt', 'w') as f:
                f.writelines(transaction_list.__str__())
            break

        case 'compare':
            print("\n%-10s %15s %15s %15s %15s" %("TICKER", "SHARE_PRICE",  "CURRENT", "TARGET", "SHORTFALL"))
            for key in portfolio.positions:
                percentage_held = stringify_percentage(portfolio.percentage_held(key))
                shortfall = stringify_percentage(allocations_dict[key]-portfolio.percentage_held(key))
                share_price = stringify_dollar(portfolio.positions[key].share_price)
                target_allocation = stringify_percentage(allocations_dict[key])
                print("%-10s %15s %15s %15s %15s" %(key, share_price, percentage_held, target_allocation, shortfall))
            
        case 'allocate':
            allocation_ticker = ""
            shortfall = 0.0
            try: 
                allocation_ticker = input("\nEnter ticker: ").upper()
                shortfall = allocations_dict[allocation_ticker]-portfolio.percentage_held(allocation_ticker)
            except KeyError:
                print("Could not find ticker in portfolio")
                print("")
                continue
            percentage_allo = shortfall
            dollar_allo = shortfall*portfolio.total
            share_price = portfolio.positions[allocation_ticker].share_price
            shares = dollar_allo/share_price
            print("\n%-15s %-15s %-15s" %("ALLO_AMOUNT", "ALLO_PER", "ALLOW_SHARES"))
            print("%-15s %-15s %-15s" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))
            if shortfall < 0:
                print("\nmust be under allocated to submit allocation")
            else:
                if dollar_allo > transaction_list.current_allocation_ammount:
                    print("\nFull allocation requires more than amount to allocate. Will only allocate up to amount can.  New values")
                    dollar_allo = transaction_list.current_allocation_ammount
                    percentage_allo = dollar_allo/portfolio.total
                    shares = dollar_allo/share_price
                    print("\n%-15s %-15s %-15s" %("ALLO_AMOUNT", "ALLO_PER", "ALLOW_SHARES"))
                    print("%-15s %-15s %-15s" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))
                
                shares = float(input("How many shares should be purchased? "))
                dollar_allo = share_price * shares
                percentage_allo = dollar_allo/portfolio.total

                print("New values")
                print("\n%-15s %-15s %-15s" %("ALLO_AMOUNT", "ALLO_PER", "ALLOW_SHARES"))
                print("%-15s %-15s %-15s" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))
                confirm = input("\nconfirm allocation (y/n)? ")
                if confirm.lower() == "y":
                    try:
                        transaction_list.add_transaction(allocation_ticker, Transaction(shares, dollar_allo))
                    except KeyError:
                        print("Transaction for ticker exists, use upd_trn")

        case 'sell':
            allocation_ticker = ""
            over_allocation = 0.0
            try: 
                allocation_ticker = input("\nEnter ticker: ").upper()
                over_allocation = portfolio.percentage_held(allocation_ticker) - allocations_dict[allocation_ticker]
            except KeyError:
                print("Could not find ticker in portfolio")
                print("")
                continue
            percentage_allo = over_allocation
            dollar_allo = over_allocation*portfolio.total
            share_price = portfolio.positions[allocation_ticker].share_price
            shares = dollar_allo/share_price
            shares = float(input("How many shares should be purchased? "))
            dollar_allo = share_price * shares
            percentage_allo = dollar_allo/portfolio.total
            
            print("\n%-15s %-15s %-15s" %("OVER_AMOUNT", "OVER_PER", "OVER_SHARES"))
            print("%-15s %-15s %-15s" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))
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

        case 'rmv_trn':
            ticker = input("Enter ticker to remove: ").upper()
            transaction_list.rmv_transaction(ticker)
        
        case 'upd_trn':
            ticker = input("Enter ticker to update: ").upper()
            try:
                shares = float(input("Enter number of shares: "))
                cost = portfolio.positions[ticker].share_price * shares
                transaction_list.upd_transaction(ticker, Transaction(shares, cost))
            except KeyError:
                print("Could not find ticker for entered value")

        case 'help':
            # TODO, move the strings to a readme file of sorts and print from the readme
            print("\n%-10s %-15s" %("allocate", "Allocate portion of cash to a specific transaction"))
            print("%-10s %-15s" %("compare", "Shows the current state of portfolio versus the target state"))
            print("%-10s %-15s" %("exit", "Close CLI and print dump of transaction list to dump.txt"))
            print("%-10s %-15s" %("reset", "Reset the state back to what it was on system startup"))
            print("%-10s %-15s" %("rmv_trn", "Remove a specific transaction from transaction list"))
            print("%-10s %-15s" %("trans", "Check the current list of all transactions to execute"))
            print("%-10s %-15s" %("upd_trn", "Update an existing transaction"))
        
        case _:
            print("Command not found")

    print("")
