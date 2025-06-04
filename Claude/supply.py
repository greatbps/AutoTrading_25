import logging

logger = logging.getLogger(__name__)

class MarketSupplyDemand:
    def __init__(self, kiwoom_api):
        self.api = kiwoom_api

    def check_institutional_buying(self, code):
        logger.info(f"{code} 외인+기관 수급 확인")
        return True

    def check_program_buying(self, code):
        logger.info(f"{code} 프로그램 매수 확인")
        return True
