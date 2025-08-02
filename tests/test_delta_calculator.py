import pytest
import math
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from delta_calculator import OptionCalculator


class TestDeltaCalculator:
    
    def test_shouldCalculateCallOptionDelta_basicBlackScholes(self):
        """Test basic call option delta calculation using Black-Scholes formula"""
        calculator = OptionCalculator()
        
        # Standard test case: ATM call option
        underlying_price = 100.0
        strike_price = 100.0
        time_to_expiry = 0.25  # 3 months
        risk_free_rate = 0.05  # 5%
        volatility = 0.20  # 20%
        
        delta = calculator.calculate_call_delta(
            underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        # ATM call delta should be approximately 0.569 for these parameters
        assert abs(delta - 0.569) < 0.01, f"Expected delta around 0.569, got {delta}"
    
    def test_shouldCalculatePutOptionDelta_basicBlackScholes(self):
        """Test basic put option delta calculation using Black-Scholes formula"""
        calculator = OptionCalculator()
        
        # Standard test case: ATM put option
        underlying_price = 100.0
        strike_price = 100.0
        time_to_expiry = 0.25  # 3 months
        risk_free_rate = 0.05  # 5%
        volatility = 0.20  # 20%
        
        delta = calculator.calculate_put_delta(
            underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility
        )
        
        # ATM put delta should be approximately -0.431 (call delta - 1)
        assert abs(delta - (-0.431)) < 0.01, f"Expected delta around -0.431, got {delta}"

    def test_shouldCalculateQQQHedgeQuantity_simpleTQQQCall(self):
        """Test calculating required QQQ hedge quantity for a short TQQQ call position"""
        calculator = OptionCalculator()
        
        # TQQQ short call position
        tqqq_price = 45.0
        tqqq_strike = 46.0  # Slightly OTM call
        tqqq_quantity = -10  # Short 10 contracts
        
        # QQQ hedge option (far OTM)
        qqq_price = 370.0  # QQQ typically trades around 370 when TQQQ is 45
        qqq_strike = 380.0  # Far OTM hedge
        
        # Common parameters
        time_to_expiry = 0.019  # Weekly options (~1 week)
        risk_free_rate = 0.05
        volatility = 0.25
        
        hedge_quantity = calculator.calculate_hedge_quantity(
            tqqq_price=tqqq_price,
            tqqq_strike=tqqq_strike,
            tqqq_quantity=tqqq_quantity,
            tqqq_option_type='call',
            qqq_price=qqq_price,
            qqq_strike=qqq_strike,
            qqq_option_type='call',
            time_to_expiry=time_to_expiry,
            risk_free_rate=risk_free_rate,
            volatility=volatility
        )
        
        # Should return positive quantity to buy QQQ calls to hedge short TQQQ calls
        assert hedge_quantity > 0, f"Expected positive hedge quantity, got {hedge_quantity}"
        # Should be reasonable multiple of TQQQ position due to leverage difference
        assert 5 < hedge_quantity < 50, f"Expected hedge quantity between 5-50, got {hedge_quantity}" 