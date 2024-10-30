from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Adding AAPL as the asset of interest for this strategy
        self.tickers = ["AAPL"]

    @property
    def assets(self):
        # Defining the assets used in the strategy
        return self.tickers

    @property
    def interval(self):
        # Defining the interval for data fetching, "1day" for daily RSI values
        return "1day"

    def run(self, data):
        # Default to no allocation
        allocation_dict = {"AAPL": 0}
        
        # Checking if there's enough data for AAPL to compute RSI
        if "AAPL" in data["ohlcv"]:
            aapl_data = data["ohlcv"]["AAPL"]
            if len(aapl_data) > 14:  # Ensuring there's enough data for the RSI calculation
                # Compute the RSI for AAPL
                rsi_values = RSI("AAPL", aapl_data, length=14)  # Standard period for RSI is 14
                latest_rsi = rsi_values[-1]  # Get the latest RSI value

                log(f"AAPL latest RSI: {latest_rsi}")

                # Buy signal: RSI < 30
                if latest_rsi < 30:
                    allocation_dict["AAPL"] = 1  # Taking a full position

                # The strategy does not take any position if RSI > 70,
                # considering it overbought, thus allocation remains 0

        # Returning target allocation based on RSI logic
        return TargetAllocation(allocation_dict)