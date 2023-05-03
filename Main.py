# Things left to clean up can improve
# Could make portfolio into it's own class
# Add a way to remove transactions
# Work on a selling interface as well

BOND_TICKERS = ('BND', 'SCHZ', 'AGG') 

import csv
from Formatting import stringify_dollar, stringify_percentage
from Data_Manipulation import reduce_dictionary, combine_tickers
from Build_Dictionaries import retrieve_portfolio, retrieve_portfolio_total, retrieve_allocations

account_total = retrieve_portfolio_total()
portfolio = retrieve_portfolio()
allocations_dict = retrieve_allocations()

# Reduces Bond tickers to just BND, might want make generic method at some point
bnd_per = combine_tickers(BOND_TICKERS, reduce_dictionary(portfolio, 1))
portfolio['BND'][0] = stringify_percentage(bnd_per)
portfolio['BND'][1] = bnd_per
vti_per = portfolio['VTI'][1] / 2
portfolio['AVUS'][0] = stringify_percentage(vti_per+portfolio['AVUS'][1])
portfolio['AVUS'][1] = vti_per+portfolio['AVUS'][1]
portfolio['DFUS'][0] = stringify_percentage(vti_per+portfolio['DFUS'][1])
portfolio['DFUS'][1] = vti_per+portfolio['DFUS'][1]
portfolio.pop('VTI')
for ticker in BOND_TICKERS:
    if ticker != 'BND':
        portfolio.pop(ticker)

base_allocation_amount = (portfolio['CASH'][1] - allocations_dict['CASH'])*account_total
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
            # TODO shortfall dollar amount and per, probably replace share price
            for key in portfolio:
                shortfall = stringify_percentage(allocations_dict[key]-portfolio[key][1])
                print("%-10s %15s %15s %15s %15s" %(key, portfolio[key][2], portfolio[key][0], stringify_percentage(allocations_dict[key]), shortfall))
        case 'allocate':
            allocation_ticker = input("\nEnter ticker: ").upper()
            shortfall = allocations_dict[allocation_ticker]-portfolio[allocation_ticker][1]
            percentage_allo = shortfall
            dollar_allo = shortfall*account_total
            share_price = portfolio[allocation_ticker][3]
            shares = dollar_allo/share_price
            print("\n%-15s %-15s %-15s" %("ALLO_AMOUNT", "ALLO_PER", "ALLOW_SHARES"))
            print("%-15s %-15s %-15s" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))
            if shortfall < 0:
                print("\nmust be under allocated to submit allocation")
            else:
                if dollar_allo > current_allocation_ammount:
                    print("\nFull allocation requires more than amount to allocate. Will only allocate up to amount can.  New values")
                    dollar_allo = current_allocation_ammount
                    percentage_allo = dollar_allo/account_total
                    shares = dollar_allo/share_price
                    print("\n%-15s %-15s %-15s" %("ALLO_AMOUNT", "ALLO_PER", "ALLOW_SHARES"))
                    print("%-15s %-15s %-15s" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))
                
                shares = float(input("How many shares should be purchased? "))
                dollar_allo = share_price * shares
                percentage_allo = dollar_allo/account_total

                print("New values")
                print("\n%-15s %-15s %-15s" %("ALLO_AMOUNT", "ALLO_PER", "ALLOW_SHARES"))
                print("%-15s %-15s %-15s" %(stringify_dollar(dollar_allo), stringify_percentage(percentage_allo), str(round(shares,2))))
                confirm = input("\nconfirm allocation (y/n)? ")
                if confirm.lower() == "y":
                    transaction_list[allocation_ticker] = [shares, dollar_allo, percentage_allo]
                    current_allocation_ammount = current_allocation_ammount - dollar_allo
            # TODO can create exception for ticker not found
        case 'reset':
            current_allocation_ammount = base_allocation_amount
        case 'trans':
            print("\nBase allocation amount")
            print("Dollars: " + stringify_dollar(base_allocation_amount))
            print("Percentage: " + stringify_percentage(base_allocation_amount/account_total))

            print("\nUnallocated amount")
            print("Dollars: " + stringify_dollar(current_allocation_ammount))
            print("Percentage: " + stringify_percentage(current_allocation_ammount/account_total))

            print("\nAllocations")
            print("%-10s %15s %15s %15s" %("TICKER", "SHARES",  "DOLLAR", "PERCENTAGE"))
            total_dollar = 0.0
            total_percentage = 0.0
            for key in transaction_list:
                dollar_amt = stringify_dollar(transaction_list[key][1])
                shares = transaction_list[key][0]
                percentage_amt = stringify_percentage(transaction_list[key][2])
                total_dollar = total_dollar + transaction_list[key][1]
                total_percentage = total_percentage + transaction_list[key][2]
                print("%-10s %15s %15s %15s" %(key,  shares, dollar_amt, percentage_amt))
            print("%-10s %15s %15s %15s" %("TOTALS",  "", stringify_dollar(total_dollar), stringify_percentage(total_percentage)))
        # TODO, default case???
    print("")
    
