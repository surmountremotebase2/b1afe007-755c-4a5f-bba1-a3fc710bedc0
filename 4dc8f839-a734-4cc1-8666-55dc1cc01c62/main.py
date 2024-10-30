from surmount.base_class import Strategy, TargetAllocation
from surmount.data import SocialSentiment, Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TWTR", "FB"]  # Example tickers
        self.data_list = [SocialSentiment(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            sentiment_data = data[("social_sentiment", ticker)]
            if sentiment_data and len(sentiment_data) > 0:
                # Example: Short if negative sentiment increase, else neutral
                sentiment = sentiment_data[-1]['twitterSentiment']
                previous_sentiment = sentiment_data[-2]['twitterSentiment'] if len(sentiment_data) > 1 else sentiment
                
                if sentiment < previous_sentiment:  # Assuming negative sentiment worsens
                    allocation_dict[ticker] = -1 / len(self.tickers)  # Short position signified by negative
                else:
                    allocation_dict[ticker] = 0  # No position
            else:
                allocation_dict[ticker] = 0  # No data, no position
            
            log(f"Allocation for {ticker}: {allocation_dict[ticker]} based on sentiment analysis")

        return TargetAllocation(allocation_dict)