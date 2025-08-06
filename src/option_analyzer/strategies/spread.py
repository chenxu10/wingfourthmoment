"""
Spread option strategies
"""

import numpy as np
from typing import Tuple

from ..models import StrategyConfig
from ..pricing import BlackScholesCalculator
from .base import OptionStrategy


class SpreadStrategy(OptionStrategy):
    """Spread strategies (S1-S24, excluding Iron Condors)"""
    
    def __init__(self, config: StrategyConfig, base_price: float = 100.0):
        self.config = config
        self.base_price = base_price
        self.calculator = BlackScholesCalculator()
        self.risk_free_rate = 0.05
        self.volatility = 0.25
        
        # Set time to expiration based on time frame
        self.time_to_expiration = self._get_time_to_expiration()
        
        # Get spread strikes instead of single strike
        self.long_strike, self.short_strike = self._get_spread_strikes()
    
    def _get_time_to_expiration(self) -> float:
        """Get time to expiration based on time frame"""
        time_map = {
            "Near": 30 / 365,    # 30 days
            "Medium": 60 / 365,  # 60 days  
            "Long": 120 / 365    # 120 days
        }
        return time_map.get(self.config.time_frame, 30 / 365)
    
    @property
    def strike_price(self) -> str:
        """Return a string representation of the spread strikes"""
        return f"{self.short_strike:.0f}/{self.long_strike:.0f}"
    
    def _get_spread_strikes(self) -> Tuple[float, float]:
        """Get strike prices for spread strategies"""
        if "Bull Call" in self.config.name:
            # Buy lower strike, sell higher strike
            long_strike = self.base_price * 0.98
            short_strike = self.base_price * 1.02
        elif "Bear Call" in self.config.name:
            # Sell lower strike, buy higher strike
            long_strike = self.base_price * 1.02
            short_strike = self.base_price * 0.98
        elif "Bull Put" in self.config.name:
            # Sell higher strike, buy lower strike
            long_strike = self.base_price * 0.98
            short_strike = self.base_price * 1.02
        elif "Bear Put" in self.config.name:
            # Buy higher strike, sell lower strike
            long_strike = self.base_price * 1.02
            short_strike = self.base_price * 0.98
        else:
            # Default spread
            long_strike = self.base_price * 0.98
            short_strike = self.base_price * 1.02
        
        return long_strike, short_strike
    
    def calculate_payoff(self, stock_prices: np.ndarray, time_to_exp: float = None) -> np.ndarray:
        """Calculate payoff for spread strategies"""
        if "Call" in self.config.name:
            if "Bull" in self.config.name:
                # Bull call spread: Buy lower strike, sell higher strike (Net Debit)
                long_payoffs = np.maximum(stock_prices - self.long_strike, 0)
                short_payoffs = np.maximum(stock_prices - self.short_strike, 0)
                return long_payoffs - short_payoffs - self.get_initial_cost()
            else:
                # Bear call spread: Sell lower strike, buy higher strike (Net Credit)  
                long_payoffs = np.maximum(stock_prices - self.long_strike, 0)
                short_payoffs = np.maximum(stock_prices - self.short_strike, 0)
                return self.get_initial_cost() - (short_payoffs - long_payoffs)
        else:
            # Put spreads
            if "Bull" in self.config.name:
                # Bull put spread: Sell higher strike, buy lower strike (Net Credit)
                # We collect credit upfront, lose money if puts go ITM
                long_payoffs = np.maximum(self.long_strike - stock_prices, 0)   # Put we own (lower strike)
                short_payoffs = np.maximum(self.short_strike - stock_prices, 0) # Put we sold (higher strike)
                # P&L = Credit received - (what we owe on short put - what we get from long put)
                return self.get_initial_cost() - (short_payoffs - long_payoffs)
            else:
                # Bear put spread: Buy higher strike, sell lower strike (Net Debit)
                long_payoffs = np.maximum(self.long_strike - stock_prices, 0)
                short_payoffs = np.maximum(self.short_strike - stock_prices, 0)  
                return long_payoffs - short_payoffs - self.get_initial_cost()
    
    def get_initial_cost(self) -> float:
        # Simplified calculation
        if "Call" in self.config.name:
            long_premium = self.calculator.calculate_call_price(
                self.base_price, self.long_strike, self.time_to_expiration,
                self.risk_free_rate, self.volatility
            )
            short_premium = self.calculator.calculate_call_price(
                self.base_price, self.short_strike, self.time_to_expiration,
                self.risk_free_rate, self.volatility
            )
        else:
            long_premium = self.calculator.calculate_put_price(
                self.base_price, self.long_strike, self.time_to_expiration,
                self.risk_free_rate, self.volatility
            )
            short_premium = self.calculator.calculate_put_price(
                self.base_price, self.short_strike, self.time_to_expiration,
                self.risk_free_rate, self.volatility
            )
        
        if "Bull Call" in self.config.name or "Bear Put" in self.config.name:
            return long_premium - short_premium  # Net debit (positive = money paid)
        else:
            return short_premium - long_premium  # Net credit (positive = money received) 