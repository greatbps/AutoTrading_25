import logging

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, max_position_ratio=0.1, max_daily_loss=0.05):
        self.max_position_ratio = max_position_ratio
        self.max_daily_loss = max_daily_loss

    def check_position_size(self, position_value, portfolio_value):
        ratio = position_value / portfolio_value
        return ratio <= self.max_position_ratio

    def check_daily_loss_limit(self, pnl, portfolio_value):
        if pnl < 0:
            return abs(pnl) / portfolio_value <= self.max_daily_loss
        return True
