"""
Iron Condor option strategy
"""

import numpy as np
from typing import Tuple

from ..models import StrategyConfig
from ..pricing import BlackScholesCalculator
from .base import OptionStrategy


class IronCondorStrategy(OptionStrategy):
    """Iron Condor strategy (4-leg neutral strategy)"""
    
    def __init__(self, config: StrategyConfig, base_price: float = 100.0):
        self.config = config
        self.base_price = base_price
        self.calculator = BlackScholesCalculator()
        self.risk_free_rate = 0.05
        self.volatility = 0.25
        
        # Set time to expiration based on time frame
        self.time_to_expiration = self._get_time_to_expiration()
        
        # Get all 4 strikes for Iron Condor
        self.put_long_strike, self.put_short_strike, self.call_short_strike, self.call_long_strike = self._get_iron_condor_strikes()
    
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
        """Return a string representation of all 4 Iron Condor strikes"""
        return f"{self.put_long_strike:.0f}/{self.put_short_strike:.0f}/{self.call_short_strike:.0f}/{self.call_long_strike:.0f}"
    
    def _get_iron_condor_strikes(self) -> Tuple[float, float, float, float]:
        """Get all 4 strike prices for Iron Condor
        Returns: (put_long_strike, put_short_strike, call_short_strike, call_long_strike)
        """
        # Iron Condor strikes based on current stock price
        # Typical Iron Condor has wings about 5-10 points wide
        wing_width = self.base_price * 0.05  # 5% wing width
        
        # Put side (lower strikes)
        put_short_strike = self.base_price * 0.95   # Sell put 5% OTM
        put_long_strike = put_short_strike - wing_width  # Buy put further OTM
        
        # Call side (higher strikes) 
        call_short_strike = self.base_price * 1.05   # Sell call 5% OTM
        call_long_strike = call_short_strike + wing_width  # Buy call further OTM
        
        return put_long_strike, put_short_strike, call_short_strike, call_long_strike
    
    def calculate_payoff(self, stock_prices: np.ndarray, time_to_exp: float = None) -> np.ndarray:
        """Calculate Iron Condor payoff (4-leg strategy)"""
        if time_to_exp is None or time_to_exp <= 0:
            # At expiration - calculate intrinsic values
            # Put spread payoff (we sold put_short, bought put_long)
            put_long_payoffs = np.maximum(self.put_long_strike - stock_prices, 0)
            put_short_payoffs = np.maximum(self.put_short_strike - stock_prices, 0)
            put_spread_payoff = put_short_payoffs - put_long_payoffs  # We owe put_short, collect put_long
            
            # Call spread payoff (we sold call_short, bought call_long) 
            call_short_payoffs = np.maximum(stock_prices - self.call_short_strike, 0)
            call_long_payoffs = np.maximum(stock_prices - self.call_long_strike, 0)
            call_spread_payoff = call_short_payoffs - call_long_payoffs  # We owe call_short, collect call_long
            
            # Total payoff = credit received - what we owe
            total_payoff = self.get_initial_cost() - (put_spread_payoff + call_spread_payoff)
            return total_payoff
        else:
            # Before expiration - use Black-Scholes
            payoffs = []
            for S in stock_prices:
                # Calculate current option values
                put_long_value = self.calculator.calculate_put_price(
                    S, self.put_long_strike, time_to_exp, self.risk_free_rate, self.volatility
                )
                put_short_value = self.calculator.calculate_put_price(
                    S, self.put_short_strike, time_to_exp, self.risk_free_rate, self.volatility
                )
                call_short_value = self.calculator.calculate_call_price(
                    S, self.call_short_strike, time_to_exp, self.risk_free_rate, self.volatility
                )
                call_long_value = self.calculator.calculate_call_price(
                    S, self.call_long_strike, time_to_exp, self.risk_free_rate, self.volatility
                )
                
                # Current position value
                current_value = (put_long_value - put_short_value + call_long_value - call_short_value)
                
                # P&L = initial credit received + current position value
                pnl = self.get_initial_cost() + current_value
                payoffs.append(pnl)
            
            return np.array(payoffs)
    
    def get_initial_cost(self) -> float:
        """Get initial credit received from Iron Condor"""
        # Calculate premiums for all 4 legs
        put_long_premium = self.calculator.calculate_put_price(
            self.base_price, self.put_long_strike, self.time_to_expiration,
            self.risk_free_rate, self.volatility
        )
        put_short_premium = self.calculator.calculate_put_price(
            self.base_price, self.put_short_strike, self.time_to_expiration,
            self.risk_free_rate, self.volatility
        )
        call_short_premium = self.calculator.calculate_call_price(
            self.base_price, self.call_short_strike, self.time_to_expiration,
            self.risk_free_rate, self.volatility
        )
        call_long_premium = self.calculator.calculate_call_price(
            self.base_price, self.call_long_strike, self.time_to_expiration,
            self.risk_free_rate, self.volatility
        )
        
        # Net credit = premiums received - premiums paid
        # We sell put_short and call_short (receive premium)
        # We buy put_long and call_long (pay premium)
        net_credit = (put_short_premium + call_short_premium) - (put_long_premium + call_long_premium)
        return net_credit 