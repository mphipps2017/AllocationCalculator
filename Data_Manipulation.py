def reduce_dictionary(dictionary, col):
    new_dict = {}
    for key in dictionary:
        new_dict[key] = dictionary[key][col]
    return new_dict


# Ticker = list of tickers to combine percetnages
# Percentage = dictionary of ticker  percentage pairs
# Returns the total percentage of all tickers
def combine_tickers(tickers, percentages):
    percentage = 0
    for ticker in tickers:
        percentage = percentage + percentages[ticker]
    return percentage