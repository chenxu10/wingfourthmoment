"""
Long call option strategy
"""

import numpy as np
from .base import OptionStrategy


class LongCallStrategy(OptionStrategy):
    """Long call strategies (C1-C15)"""
    
    def calculate_payoff(self, stock_prices: np.ndarray, time_to_exp: float = None) -> np.ndarray:
        if time_to_exp is None or time_to_exp <= 0:
            # At expiration
            return np.maximum(stock_prices - self.strike_price, 0) - self.get_initial_cost()
        else:
            # Before expiration
            payoffs = []
            for S in stock_prices:
                option_value = self.calculator.calculate_call_price(
                    S, self.strike_price, time_to_exp, self.risk_free_rate, self.volatility
                )
                payoffs.append(option_value - self.get_initial_cost())
            return np.array(payoffs)
    
    def get_initial_cost(self) -> float:
        return self.calculator.calculate_call_price(
            self.base_price, self.strike_price, self.time_to_expiration, 
            self.risk_free_rate, self.volatility
        ) 