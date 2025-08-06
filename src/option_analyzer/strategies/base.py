"""
Base option strategy class
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import Dict

from ..models import StrategyConfig
from ..pricing import BlackScholesCalculator


class OptionStrategy(ABC):
    """Abstract base class for options strategies"""
    
    def __init__(self, config: StrategyConfig, base_price: float = 100.0):
        self.config = config
        self.base_price = base_price
        self.calculator = BlackScholesCalculator()
        self.risk_free_rate = 0.05
        self.volatility = 0.25
        
        # Set time to expiration based on time frame
        self.time_to_expiration = self._get_time_to_expiration()
        
        # Set strike price based on moneyness
        self.strike_price = self._get_strike_price()
        
    def _get_time_to_expiration(self) -> float:
        """Get time to expiration based on time frame"""
        time_map = {
            "Near": 30 / 365,    # 30 days
            "Medium": 60 / 365,  # 60 days  
            "Long": 120 / 365    # 120 days
        }
        return time_map.get(self.config.time_frame, 30 / 365)
    
    def _get_strike_price(self) -> float:
        """Get strike price based on moneyness"""
        moneyness_map = {
            "Deep OTM": 0.90 if "call" in self.config.strategy_type.lower() else 1.10,
            "Shallow OTM": 0.95 if "call" in self.config.strategy_type.lower() else 1.05,
            "ATM": 1.00,
            "Shallow ITM": 1.05 if "call" in self.config.strategy_type.lower() else 0.95,
            "Deep ITM": 1.10 if "call" in self.config.strategy_type.lower() else 0.90
        }
        multiplier = moneyness_map.get(self.config.moneyness, 1.00)
        return self.base_price * multiplier
    
    @abstractmethod
    def calculate_payoff(self, stock_prices: np.ndarray, time_to_exp: float = None) -> np.ndarray:
        """Calculate strategy payoff for given stock prices"""
        pass
    
    @abstractmethod
    def get_initial_cost(self) -> float:
        """Get initial cost/credit of the strategy"""
        pass
    
    def calculate_greeks(self) -> Dict[str, float]:
        """Calculate Greeks for the strategy"""
        return {
            "delta": 0.0,
            "theta": 0.0, 
            "vega": 0.0,
            "gamma": 0.0
        } 