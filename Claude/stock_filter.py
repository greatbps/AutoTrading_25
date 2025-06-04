import logging

logger = logging.getLogger(__name__)

class StockFilter:
    def __init__(self, kiwoom_api):
        self.api = kiwoom_api

    def get_top_volume_stocks(self, count=20):
        logger.info(f"거래대금 상위 {count}개 종목 조회")
        return []

    def get_top_rising_stocks(self, count=20):
        logger.info(f"급등률 상위 {count}개 종목 조회")
        return []

    def filter_by_criteria(self, stock_codes):
        logger.info("필터 조건 적용 시작")
        return stock_codes
