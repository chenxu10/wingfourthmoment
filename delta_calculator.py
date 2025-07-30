import math
from scipy.stats import norm


class OptionCalculator:
    """Calculator for option Greeks and hedging ratios between QQQ and TQQQ"""
    
    def calculate_call_delta(self, underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility):
        """Calculate call option delta using Black-Scholes formula"""
        if time_to_expiry <= 0:
            return 1.0 if underlying_price > strike_price else 0.0
            
        d1 = (math.log(underlying_price / strike_price) + 
              (risk_free_rate + 0.5 * volatility**2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
        
        return norm.cdf(d1)
    
    def calculate_put_delta(self, underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility):
        """Calculate put option delta using Black-Scholes formula"""
        call_delta = self.calculate_call_delta(underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility)
        return call_delta - 1.0
    
    def calculate_hedge_quantity(self, tqqq_price, tqqq_strike, tqqq_quantity, tqqq_option_type,
                               qqq_price, qqq_strike, qqq_option_type, time_to_expiry, 
                               risk_free_rate, volatility):
        """Calculate required QQQ hedge quantity for TQQQ position to maintain delta neutrality"""
        # Calculate TQQQ option delta
        if tqqq_option_type.lower() == 'call':
            tqqq_delta = self.calculate_call_delta(tqqq_price, tqqq_strike, time_to_expiry, risk_free_rate, volatility)
        else:
            tqqq_delta = self.calculate_put_delta(tqqq_price, tqqq_strike, time_to_expiry, risk_free_rate, volatility)
        
        # Calculate QQQ option delta
        if qqq_option_type.lower() == 'call':
            qqq_delta = self.calculate_call_delta(qqq_price, qqq_strike, time_to_expiry, risk_free_rate, volatility)
        else:
            qqq_delta = self.calculate_put_delta(qqq_price, qqq_strike, time_to_expiry, risk_free_rate, volatility)
        
        # TQQQ is 3x leveraged, so 1 point move in NDX100 = 3 points in TQQQ, 1 point in QQQ
        # Leverage adjustment factor
        leverage_ratio = 3.0
        
        # Calculate total delta exposure from TQQQ position
        tqqq_total_delta = tqqq_quantity * tqqq_delta * leverage_ratio
        
        # Calculate required QQQ quantity to neutralize this delta
        # We want: tqqq_total_delta + qqq_quantity * qqq_delta = 0
        # So: qqq_quantity = -tqqq_total_delta / qqq_delta
        if abs(qqq_delta) < 1e-10:  # Avoid division by zero
            return 0.0
            
        qqq_hedge_quantity = -tqqq_total_delta / qqq_delta
        
        return qqq_hedge_quantity 