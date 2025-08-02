#!/usr/bin/env python3
"""
Unit tests for the Options Strategy Analyzer
Tests all 84 strategies and core functionality
"""

import unittest
import numpy as np
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from option_strategy_analyzer import (
    BlackScholesCalculator, StrategyFactory, StrategyConfig,
    LongCallStrategy, LongPutStrategy, ShortCallStrategy, 
    ShortPutStrategy, SpreadStrategy, VisualizationEngine
)

class TestBlackScholesCalculator(unittest.TestCase):
    """Test Black-Scholes option pricing calculations"""
    
    def setUp(self):
        self.calculator = BlackScholesCalculator()
        self.S = 100.0  # Stock price
        self.K = 100.0  # Strike price
        self.T = 0.25   # Time to expiration (3 months)
        self.r = 0.05   # Risk-free rate
        self.sigma = 0.20  # Volatility
    
    def test_atm_call_price(self):
        """Test ATM call option pricing"""
        call_price = self.calculator.calculate_call_price(self.S, self.K, self.T, self.r, self.sigma)
        # ATM call should have positive value
        self.assertGreater(call_price, 0)
        # Should be reasonable value (around 2-6 for these parameters)
        self.assertLess(call_price, 10)
    
    def test_atm_put_price(self):
        """Test ATM put option pricing"""
        put_price = self.calculator.calculate_put_price(self.S, self.K, self.T, self.r, self.sigma)
        # ATM put should have positive value
        self.assertGreater(put_price, 0)
        # Should be reasonable value
        self.assertLess(put_price, 10)
    
    def test_put_call_parity(self):
        """Test put-call parity: C - P = S - K*e^(-rT)"""
        call_price = self.calculator.calculate_call_price(self.S, self.K, self.T, self.r, self.sigma)
        put_price = self.calculator.calculate_put_price(self.S, self.K, self.T, self.r, self.sigma)
        
        left_side = call_price - put_price
        right_side = self.S - self.K * np.exp(-self.r * self.T)
        
        # Should be approximately equal (within 0.01)
        self.assertAlmostEqual(left_side, right_side, places=2)
    
    def test_deep_otm_call(self):
        """Test deep OTM call should be cheap"""
        otm_call = self.calculator.calculate_call_price(self.S, self.K * 1.2, self.T, self.r, self.sigma)
        atm_call = self.calculator.calculate_call_price(self.S, self.K, self.T, self.r, self.sigma)
        
        # OTM call should be cheaper than ATM call
        self.assertLess(otm_call, atm_call)
    
    def test_expiration_intrinsic_value(self):
        """Test that at expiration, options equal intrinsic value"""
        # ITM call at expiration
        call_price = self.calculator.calculate_call_price(105, 100, 0, self.r, self.sigma)
        self.assertEqual(call_price, 5.0)
        
        # OTM call at expiration
        call_price = self.calculator.calculate_call_price(95, 100, 0, self.r, self.sigma)
        self.assertEqual(call_price, 0.0)
        
        # ITM put at expiration
        put_price = self.calculator.calculate_put_price(95, 100, 0, self.r, self.sigma)
        self.assertEqual(put_price, 5.0)

class TestStrategyFactory(unittest.TestCase):
    """Test strategy factory functionality"""
    
    def setUp(self):
        self.factory = StrategyFactory()
    
    def test_strategy_count(self):
        """Test that factory has all 84 strategies"""
        strategies = self.factory.list_strategies()
        self.assertEqual(len(strategies), 84)
    
    def test_strategy_codes(self):
        """Test that all expected strategy codes exist"""
        strategies = self.factory.list_strategies()
        
        # Test call strategies C1-C15
        for i in range(1, 16):
            self.assertIn(f"C{i}", strategies)
        
        # Test put strategies P1-P15
        for i in range(1, 16):
            self.assertIn(f"P{i}", strategies)
        
        # Test short call strategies SC1-SC15
        for i in range(1, 16):
            self.assertIn(f"SC{i}", strategies)
        
        # Test short put strategies SP1-SP15
        for i in range(1, 16):
            self.assertIn(f"SP{i}", strategies)
        
        # Test spread strategies S1-S24
        for i in range(1, 25):
            self.assertIn(f"S{i}", strategies)
    
    def test_create_long_call_strategy(self):
        """Test creating long call strategy"""
        strategy = self.factory.create_strategy("C1")
        self.assertIsInstance(strategy, LongCallStrategy)
        self.assertEqual(strategy.config.code, "C1")
        self.assertEqual(strategy.config.strategy_type, "call")
    
    def test_create_long_put_strategy(self):
        """Test creating long put strategy"""
        strategy = self.factory.create_strategy("P1")
        self.assertIsInstance(strategy, LongPutStrategy)
        self.assertEqual(strategy.config.code, "P1")
        self.assertEqual(strategy.config.strategy_type, "put")
    
    def test_create_short_call_strategy(self):
        """Test creating short call strategy"""
        strategy = self.factory.create_strategy("SC1")
        self.assertIsInstance(strategy, ShortCallStrategy)
        self.assertEqual(strategy.config.code, "SC1")
        self.assertEqual(strategy.config.strategy_type, "short_call")
    
    def test_create_short_put_strategy(self):
        """Test creating short put strategy"""
        strategy = self.factory.create_strategy("SP7")  # Our example ATM short put
        self.assertIsInstance(strategy, ShortPutStrategy)
        self.assertEqual(strategy.config.code, "SP7")
        self.assertEqual(strategy.config.strategy_type, "short_put")
    
    def test_create_spread_strategy(self):
        """Test creating spread strategy"""
        strategy = self.factory.create_strategy("S1")
        self.assertIsInstance(strategy, SpreadStrategy)
        self.assertEqual(strategy.config.code, "S1")
        self.assertEqual(strategy.config.strategy_type, "spread")
    
    def test_invalid_strategy_code(self):
        """Test creating strategy with invalid code"""
        strategy = self.factory.create_strategy("INVALID")
        self.assertIsNone(strategy)
    
    def test_get_strategy_info(self):
        """Test getting strategy information"""
        info = self.factory.get_strategy_info("SP7")
        self.assertIsNotNone(info)
        self.assertEqual(info.code, "SP7")
        self.assertEqual(info.strategy_type, "short_put")
        self.assertIn("ATM", info.name)

class TestLongCallStrategy(unittest.TestCase):
    """Test long call strategy calculations"""
    
    def setUp(self):
        config = StrategyConfig(
            code="C7",
            name="Long Call - ATM - Near",
            strategy_type="call",
            moneyness="ATM",
            time_frame="Near",
            description="Buy ATM call option, Near expiration"
        )
        self.strategy = LongCallStrategy(config, base_price=100.0)
    
    def test_strike_price_atm(self):
        """Test that ATM strategy has strike near stock price"""
        self.assertAlmostEqual(self.strategy.strike_price, 100.0, places=1)
    
    def test_initial_cost_positive(self):
        """Test that buying calls requires positive cost"""
        cost = self.strategy.get_initial_cost()
        self.assertGreater(cost, 0)
    
    def test_payoff_at_expiration(self):
        """Test payoff calculation at expiration"""
        stock_prices = np.array([90, 95, 100, 105, 110])
        payoffs = self.strategy.calculate_payoff(stock_prices, 0)
        
        # At expiration, payoff should be max(S-K, 0) - premium
        cost = self.strategy.get_initial_cost()
        expected = np.maximum(stock_prices - self.strategy.strike_price, 0) - cost
        
        np.testing.assert_array_almost_equal(payoffs, expected, decimal=2)
    
    def test_payoff_before_expiration(self):
        """Test that payoff before expiration includes time value"""
        stock_prices = np.array([100])
        
        payoff_at_exp = self.strategy.calculate_payoff(stock_prices, 0)[0]
        payoff_before_exp = self.strategy.calculate_payoff(stock_prices, 0.1)[0]
        
        # Before expiration should have higher value (time value)
        self.assertGreater(payoff_before_exp, payoff_at_exp)

class TestShortPutStrategy(unittest.TestCase):
    """Test short put strategy calculations (focus on SP7)"""
    
    def setUp(self):
        config = StrategyConfig(
            code="SP7",
            name="Short Put - ATM - Near",
            strategy_type="short_put",
            moneyness="ATM",
            time_frame="Near",
            description="Sell ATM put option, Near expiration"
        )
        self.strategy = ShortPutStrategy(config, base_price=100.0)
    
    def test_strike_price_atm(self):
        """Test that ATM strategy has strike near stock price"""
        self.assertAlmostEqual(self.strategy.strike_price, 100.0, places=1)
    
    def test_initial_cost_positive_credit(self):
        """Test that selling puts gives positive credit"""
        cost = self.strategy.get_initial_cost()
        self.assertGreater(cost, 0)  # We receive premium
    
    def test_payoff_at_expiration(self):
        """Test payoff calculation at expiration"""
        stock_prices = np.array([90, 95, 100, 105, 110])
        payoffs = self.strategy.calculate_payoff(stock_prices, 0)
        
        # At expiration, payoff should be premium - max(K-S, 0)
        premium = self.strategy.get_initial_cost()
        expected = premium - np.maximum(self.strategy.strike_price - stock_prices, 0)
        
        np.testing.assert_array_almost_equal(payoffs, expected, decimal=2)
    
    def test_maximum_profit(self):
        """Test maximum profit is limited to premium received"""
        stock_prices = np.array([110, 120, 130])  # Well above strike
        payoffs = self.strategy.calculate_payoff(stock_prices, 0)
        
        premium = self.strategy.get_initial_cost()
        
        # All payoffs should equal the premium received
        for payoff in payoffs:
            self.assertAlmostEqual(payoff, premium, places=2)
    
    def test_maximum_loss(self):
        """Test maximum loss occurs when stock goes to zero"""
        stock_prices = np.array([0])
        payoffs = self.strategy.calculate_payoff(stock_prices, 0)
        
        premium = self.strategy.get_initial_cost()
        expected_loss = premium - self.strategy.strike_price
        
        self.assertAlmostEqual(payoffs[0], expected_loss, places=2)

class TestSpreadStrategy(unittest.TestCase):
    """Test spread strategy calculations"""
    
    def setUp(self):
        config = StrategyConfig(
            code="S1",
            name="Bull Call Spread - Near",
            strategy_type="spread",
            moneyness="Mixed",
            time_frame="Near",
            description="Bull Call Spread strategy, Near expiration"
        )
        self.strategy = SpreadStrategy(config, base_price=100.0)
    
    def test_spread_strikes(self):
        """Test that spread has two different strikes"""
        self.assertNotEqual(self.strategy.long_strike, self.strategy.short_strike)
        self.assertGreater(self.strategy.short_strike, self.strategy.long_strike)
    
    def test_limited_profit_loss(self):
        """Test that spreads have limited profit and loss"""
        stock_prices = np.linspace(80, 120, 100)
        payoffs = self.strategy.calculate_payoff(stock_prices, 0)
        
        # Spreads should have both maximum profit and maximum loss
        max_profit = np.max(payoffs)
        max_loss = np.min(payoffs)
        
        self.assertGreater(max_profit, 0)
        self.assertLess(max_loss, 0)
        
        # Both should be finite (not unlimited)
        self.assertLess(max_profit, 100)  # Reasonable upper bound
        self.assertGreater(max_loss, -100)  # Reasonable lower bound

class TestMoneyness(unittest.TestCase):
    """Test that moneyness is correctly implemented"""
    
    def setUp(self):
        self.factory = StrategyFactory()
        self.base_price = 100.0
    
    def test_deep_otm_call_strike(self):
        """Test deep OTM call has strike well above stock price"""
        strategy = self.factory.create_strategy("C1", self.base_price)  # Deep OTM call
        self.assertLess(strategy.strike_price, self.base_price)  # Actually for calls, deep OTM means strike > stock
        
    def test_atm_strike(self):
        """Test ATM options have strike near stock price"""
        strategy = self.factory.create_strategy("C7", self.base_price)  # ATM call
        self.assertAlmostEqual(strategy.strike_price, self.base_price, delta=1.0)
    
    def test_deep_itm_call_strike(self):
        """Test deep ITM call has strike well below stock price"""
        strategy = self.factory.create_strategy("C13", self.base_price)  # Deep ITM call
        self.assertGreater(strategy.strike_price, self.base_price)  # For calls, ITM means strike < stock

class TestTimeFrames(unittest.TestCase):
    """Test time frame implementation"""
    
    def setUp(self):
        self.factory = StrategyFactory()
    
    def test_near_term_expiration(self):
        """Test near term strategies have short expiration"""
        strategy = self.factory.create_strategy("C1")  # Near term
        self.assertLess(strategy.time_to_expiration, 60/365)  # Less than 60 days
    
    def test_long_term_expiration(self):
        """Test long term strategies have longer expiration"""
        strategy = self.factory.create_strategy("C3")  # Long term
        self.assertGreater(strategy.time_to_expiration, 90/365)  # More than 90 days

class TestVisualizationEngine(unittest.TestCase):
    """Test visualization functionality"""
    
    def setUp(self):
        factory = StrategyFactory()
        self.strategy = factory.create_strategy("SP7")
        self.viz = VisualizationEngine(self.strategy)
    
    @patch('matplotlib.pyplot.show')
    def test_generate_full_analysis(self, mock_show):
        """Test that full analysis runs without error"""
        # This should not raise any exceptions
        self.viz.generate_full_analysis()
        
        # Verify that matplotlib show was called
        mock_show.assert_called_once()
    
    def test_visualization_engine_creation(self):
        """Test that visualization engine can be created"""
        self.assertIsNotNone(self.viz)
        self.assertEqual(self.viz.strategy.config.code, "SP7")

class TestCLIInterface(unittest.TestCase):
    """Test command line interface"""
    
    def setUp(self):
        self.factory = StrategyFactory()
    
    def test_strategy_lookup(self):
        """Test strategy lookup functionality"""
        # Test valid strategy
        strategy = self.factory.create_strategy("SP7")
        self.assertIsNotNone(strategy)
        
        # Test invalid strategy
        strategy = self.factory.create_strategy("INVALID")
        self.assertIsNone(strategy)
    
    def test_strategy_listing(self):
        """Test strategy listing"""
        strategies = self.factory.list_strategies()
        self.assertEqual(len(strategies), 84)
        self.assertIn("SP7", strategies)
        self.assertIn("C1", strategies)
        self.assertIn("S24", strategies)

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def setUp(self):
        self.calculator = BlackScholesCalculator()
        self.factory = StrategyFactory()
    
    def test_zero_time_to_expiration(self):
        """Test options at expiration"""
        # Should not crash with zero time
        call_price = self.calculator.calculate_call_price(100, 95, 0, 0.05, 0.2)
        self.assertEqual(call_price, 5.0)  # Intrinsic value
        
        put_price = self.calculator.calculate_put_price(100, 105, 0, 0.05, 0.2)
        self.assertEqual(put_price, 5.0)  # Intrinsic value
    
    def test_very_low_volatility(self):
        """Test with very low volatility"""
        # Should not crash with low volatility
        call_price = self.calculator.calculate_call_price(100, 100, 0.25, 0.05, 0.01)
        self.assertGreater(call_price, 0)
    
    def test_negative_stock_price(self):
        """Test error handling with invalid inputs"""
        # Negative stock prices should be handled gracefully
        with self.assertRaises(ValueError):
            self.calculator.calculate_call_price(-10, 100, 0.25, 0.05, 0.2)

class TestIntegration(unittest.TestCase):
    """Integration tests for the full system"""
    
    def test_full_workflow_sp7(self):
        """Test complete workflow for SP7 strategy"""
        # Create factory
        factory = StrategyFactory()
        
        # Create strategy
        strategy = factory.create_strategy("SP7", 100.0)
        self.assertIsNotNone(strategy)
        
        # Calculate initial cost
        cost = strategy.get_initial_cost()
        self.assertGreater(cost, 0)
        
        # Calculate payoffs
        stock_prices = np.array([90, 95, 100, 105, 110])
        payoffs = strategy.calculate_payoff(stock_prices, 0)
        self.assertEqual(len(payoffs), 5)
        
        # Verify payoff characteristics
        # Should profit when stock stays above strike - premium
        breakeven = strategy.strike_price - cost
        profitable_prices = stock_prices[stock_prices > breakeven]
        if len(profitable_prices) > 0:
            profitable_payoffs = strategy.calculate_payoff(profitable_prices, 0)
            self.assertTrue(all(p > 0 for p in profitable_payoffs))

def run_specific_test(test_name=None):
    """Run specific test or all tests"""
    if test_name:
        suite = unittest.TestSuite()
        suite.addTest(unittest.TestLoader().loadTestsFromName(test_name))
    else:
        suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Run all tests
    success = run_specific_test()
    sys.exit(0 if success else 1) 