"""
Black-Scholes option pricing calculator
"""

import math
from scipy.stats import norm


class BlackScholesCalculator:
    """Black-Scholes option pricing calculator"""
    
    def calculate_call_price(self, S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Calculate call option price using Black-Scholes formula"""
        if T <= 0:
            return max(S - K, 0)
        
        d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
        d2 = d1 - sigma*math.sqrt(T)
        
        call_price = S*norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2)
        return max(call_price, 0)
    
    def calculate_put_price(self, S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Calculate put option price using Black-Scholes formula"""
        if T <= 0:
            return max(K - S, 0)
        
        d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
        d2 = d1 - sigma*math.sqrt(T)
        
        put_price = K*math.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
        return max(put_price, 0) 