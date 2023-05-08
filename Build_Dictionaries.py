
import csv
from Portfolio import Position, Portfolio

allocations_file_name = ""
portfolio_file_name = ""

with open('supporting_files/file_names', newline='') as file:
    lines = file.readlines()
    portfolio_file_name = lines[0].strip()
    allocations_file_name = lines[1].strip()

def retrieve_portfolio():
    portfolio_csv_dump = []
    portfolio = {}
    with open('supporting_files/'+portfolio_file_name, newline='') as csvfile:
        row_count = 0
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0
        for row in spamreader:
            portfolio_csv_dump.append(row)
            i = i + 1
        row_count = i

        # Grab account balance
        account_total = portfolio_csv_dump[row_count-1][6]
        account_total = float(account_total.strip('$').replace(',', '', len(account_total)))
        
        # create 2D array to use for calculations
        i = 0
        for row in portfolio_csv_dump:
            if i != 0 and i != 1 and i != 2 and i != row_count-1 and i != row_count-2:
                holding_per = float(row[15].strip('%'))/100
                share_price = float(row[3].strip('$').replace(',', '', len(row[3])))
                portfolio[row[0]] = Position(row[2], share_price)
            i = i + 1
        # Set cash value for portfolio
        cash = float(portfolio_csv_dump[row_count-2][6].strip('$').replace(',', '', len(portfolio_csv_dump[row_count-2][6])))
        portfolio['CASH'] = Position(cash, 1.0)
    return Portfolio(portfolio, account_total)

def retrieve_allocations():
    allocations_dict = {}
    with open('supporting_files/'+allocations_file_name, newline='') as csvfile:
        allocations = csv.reader(csvfile, delimiter=',')
        for row in allocations:
            if row[5] != "" and row[3]!="Ticker":
                allocations_dict[row[3]] = float(row[5].strip('%'))/100
    return allocations_dict