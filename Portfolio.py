from Formatting import stringify_dollar, stringify_percentage

# Shares = num shares owned
# Share_price = price per share
class Position:
    def __init__(self, shares, share_price):
        self.shares = float(shares)
        self.share_price = float(share_price)

    def str_share_price(self):
        return stringify_dollar(self.share_price)
    
    # Returns this position in dollars as a float
    def in_dollars(self):
        return self.shares * self.share_price

class Portfolio:
    def __init__(self, positions, total):
        self.positions = positions
        self.total = total
        self.condenced_positions = {}

    def remove_position(self, ticker):
        return self.positions.pop(ticker)
    
    def update_position(self, ticker, position):
        self.positions[ticker] = position
    
    def percentage_held(self, ticker):
        return self.positions[ticker].in_dollars()/self.total

    # Condences all the condencee tickers evenly over th4e condencers
    def condence_position(self, condencer_ticker, condencee_tickers):
        total = 0.0
        for ticker in condencee_tickers:
            total = total + self.positions[ticker].in_dollars()
            self.condenced_positions[ticker] = self.remove_position(ticker)

        for ticker in condencer_ticker:
            temp_total = (total)/len(condencer_ticker) + self.positions[ticker].in_dollars()
            share_price = self.positions[ticker].share_price
            shares = temp_total/share_price
            self.update_position(ticker, Position(shares, share_price))
