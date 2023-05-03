# Things left to clean up can improve
# Could make portfolio and trans into it's own class
# Add a way to remove transactions
# Work on a selling interface as well

from Formatting import stringify_dollar, stringify_percentage
from Transactions import print_transactions, Transaction
from Build_Dictionaries import retrieve_portfolio, retrieve_allocations
BOND_TICKERS = ('SCHZ', 'AGG') 

portfolio = retrieve_portfolio()
portfolio.condence_position(['BND'], BOND_TICKERS)
portfolio.condence_position(['AVUS', 'DFUS'], ['VTI'])
allocations_dict = retrieve_allocations()

base_allocation_amount = round(portfolio.positions['CASH'].in_dollars() - (allocations_dict['CASH']*portfolio.total), 2)
current_allocation_ammount = base_allocation_amount
transaction_list = {}

while True:
    command = input("Enter command: ")
    match command.lower():
        case 'exit':
            # TODO, dump trans on exit
            break
        case 'deposit':
            amount_to_allocate = input('')
        case 'bal':
            print(amount_to_allocate)
        case 'compare':
            print("\n%-10s %15s %15s %15s %15s" %("TICKER", "SHARE_PRICE",  "CURRENT", "TARGET", "SHORTFALL"))
            for key in portfolio.positions:
                percentage_held = stringify_percentage(portfolio.percentage_held(key))
                shortfall = stringify_percentage(allocations_dict[key]-portfolio.percentage_held(key))
                share_price = stringify_dollar(portfolio.positions[key].share_price)
                target_allocation = stringify_percentage(allocations_dict[key])
                print("%-10s %15s %15s %15s %15s" %(key, share_price, percentage_held, target_allocation, shortfall))
            
        case 'allocate':
            allocation_ticker = input("\nEnter ticker: ").upper()
            shortfall = allocations_dict[allocation_ticker]-portfolio.percentage_held(allocation_ticker)
            percentage_allo = shortfall
            dollar_allo = shortfall*portfolio.total
            share_price = portfolio.positions[allocation_ticker].share_price
            shares = dollar_allo/share_price
            print("\n%-15s %-15s %-15s" %("ALLO_AMOUNT", "ALLO_PER", "ALLOW_SHARES"))
            print("%-15s %-15s %-15s" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))
            if shortfall < 0:
                print("\nmust be under allocated to submit allocation")
            else:
                if dollar_allo > current_allocation_ammount:
                    print("\nFull allocation requires more than amount to allocate. Will only allocate up to amount can.  New values")
                    dollar_allo = current_allocation_ammount
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
                    transaction_list[allocation_ticker] = Transaction(shares, dollar_allo)
                    current_allocation_ammount = current_allocation_ammount - dollar_allo

            # TODO can create exception for ticker not found
        case 'reset':
            current_allocation_ammount = base_allocation_amount
        case 'trans':
            print("\nBase allocation amount")
            print("Dollars: " + stringify_dollar(base_allocation_amount))
            print("Percentage: " + stringify_percentage(base_allocation_amount/portfolio.total))

            print("\nUnallocated amount")
            print("Dollars: " + stringify_dollar(current_allocation_ammount))
            print("Percentage: " + stringify_percentage(current_allocation_ammount/portfolio.total))
            print_transactions(transaction_list, portfolio.total)
        # TODO, default case???
        case 'rmv_trn':
            ticker = input("Enter ticker to remove: ").upper()
            current_allocation_ammount = current_allocation_ammount + transaction_list[ticker][1]
            transaction_list.pop(ticker)
    print("")
