"""
Short put option strategy
"""

import numpy as np
from .base import OptionStrategy


class ShortPutStrategy(OptionStrategy):
    """Short put strategies (SP1-SP15)"""
    
    def calculate_payoff(self, stock_prices: np.ndarray, time_to_exp: float = None) -> np.ndarray:
        if time_to_exp is None or time_to_exp <= 0:
            # At expiration
            return self.get_initial_cost() - np.maximum(self.strike_price - stock_prices, 0)
        else:
            # Before expiration
            payoffs = []
            for S in stock_prices:
                option_value = self.calculator.calculate_put_price(
                    S, self.strike_price, time_to_exp, self.risk_free_rate, self.volatility
                )
                payoffs.append(self.get_initial_cost() - option_value)
            return np.array(payoffs)
    
    def get_initial_cost(self) -> float:
        # Negative cost = credit received
        return self.calculator.calculate_put_price(
            self.base_price, self.strike_price, self.time_to_expiration,
            self.risk_free_rate, self.volatility
        ) 