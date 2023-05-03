
import csv

# key               - Ticker,
# portfolio[key][0] - Percentage held (string),
# portfolio[key][1] - Percentage held (float),
# portfolio[key][2] - Share price (string),
# portfolio[key][3] - Share price (float)
def retrieve_portfolio():
    portfolio_csv_dump = []
    portfolio = {}  
    with open('TestDoc.csv', newline='') as csvfile:
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
                portfolio[row[0]] = [row[15], holding_per, row[3], share_price]
            i = i + 1

        # Set cash value for portfolio
        cash_per_str = portfolio_csv_dump[row_count-2][15]
        portfolio['CASH'] = [cash_per_str, float(cash_per_str.strip('%'))/100, "$1.00", "1"]
    return portfolio

def retrieve_portfolio_total():
    portfolio_csv_dump = []
    with open('TestDoc.csv', newline='') as csvfile:
        row_count = 0
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i = 0
        for row in spamreader:
            portfolio_csv_dump.append(row)
            i = i + 1
        row_count = i

        # Grab account balance
        account_total = portfolio_csv_dump[row_count-1][6]
    return float(account_total.strip('$').replace(',', '', len(account_total)))

def retrieve_allocations():
    allocations_dict = {}
    with open('Allocations.csv', newline='') as csvfile:
        allocations = csv.reader(csvfile, delimiter=',')
        for row in allocations:
            if row[5] != "" and row[3]!="Ticker":
                allocations_dict[row[3]] = float(row[5].strip('%'))/100
    return allocations_dict