import logging
from login import KiwoomAPI
from strategy import TradingStrategy
from risk import RiskManager
from news import NewsAnalyzer

logger = logging.getLogger(__name__)

class AutoTradingSystem:
    def __init__(self):
        self.kiwoom = KiwoomAPI()
        self.strategy = TradingStrategy(self.kiwoom)
        self.risk = RiskManager()
        self.news = NewsAnalyzer()

    def start(self):
        logger.info("자동매매 시스템 시작")
        if not self.kiwoom.login():
            logger.error("로그인 실패")
            return
        filtered = self.strategy.pre_market_filtering()
        for code in filtered:
            sentiment = self.news.analyze_news_sentiment(code, f"Company_{code}")
            logger.info(f"{code}: 뉴스 점수 {sentiment['sentiment_score']}")
