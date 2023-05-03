def reduce_dictionary(dictionary, col):
    new_dict = {}
    for key in dictionary:
        new_dict[key] = dictionary[key][col]
    return new_dict


# Ticker = list of tickers to combine percetnages
# Costs = dollar amount of positions
# Returns the total percentage of all tickers
def combine_tickers(tickers, costs):
    total = 0
    for ticker in tickers:
        total = total + costs[ticker]
    return total