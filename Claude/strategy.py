import logging
from stock_filter import StockFilter
from analyzer import TechnicalAnalyzer
from supply import MarketSupplyDemand

logger = logging.getLogger(__name__)

class TradingStrategy:
    def __init__(self, kiwoom_api):
        self.api = kiwoom_api
        self.filter = StockFilter(kiwoom_api)
        self.analyzer = TechnicalAnalyzer(kiwoom_api)
        self.supply_demand = MarketSupplyDemand(kiwoom_api)
        self.candidate_stocks = []

    def pre_market_filtering(self):
        volume_stocks = self.filter.get_top_volume_stocks()
        rising_stocks = self.filter.get_top_rising_stocks()
        all_candidates = list(set(volume_stocks + rising_stocks))
        filtered = self.filter.filter_by_criteria(all_candidates)
        self.candidate_stocks = filtered
        return filtered
