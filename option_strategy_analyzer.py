#!/usr/bin/env python3
"""
Comprehensive Options Strategy Analyzer
Supports all 84 strategies from the Options Strategy Bagua Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
import argparse
import sys
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class StrategyConfig:
    """Configuration for an options strategy"""
    code: str
    name: str
    strategy_type: str  # call, put, short_call, short_put, spread
    moneyness: str     # Deep OTM, Shallow OTM, ATM, Shallow ITM, Deep ITM
    time_frame: str    # Near, Medium, Long
    description: str

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

class LongPutStrategy(OptionStrategy):
    """Long put strategies (P1-P15)"""
    
    def calculate_payoff(self, stock_prices: np.ndarray, time_to_exp: float = None) -> np.ndarray:
        if time_to_exp is None or time_to_exp <= 0:
            # At expiration
            return np.maximum(self.strike_price - stock_prices, 0) - self.get_initial_cost()
        else:
            # Before expiration
            payoffs = []
            for S in stock_prices:
                option_value = self.calculator.calculate_put_price(
                    S, self.strike_price, time_to_exp, self.risk_free_rate, self.volatility
                )
                payoffs.append(option_value - self.get_initial_cost())
            return np.array(payoffs)
    
    def get_initial_cost(self) -> float:
        return self.calculator.calculate_put_price(
            self.base_price, self.strike_price, self.time_to_expiration,
            self.risk_free_rate, self.volatility
        )

class ShortCallStrategy(OptionStrategy):
    """Short call strategies (SC1-SC15)"""
    
    def calculate_payoff(self, stock_prices: np.ndarray, time_to_exp: float = None) -> np.ndarray:
        if time_to_exp is None or time_to_exp <= 0:
            # At expiration
            return self.get_initial_cost() - np.maximum(stock_prices - self.strike_price, 0)
        else:
            # Before expiration
            payoffs = []
            for S in stock_prices:
                option_value = self.calculator.calculate_call_price(
                    S, self.strike_price, time_to_exp, self.risk_free_rate, self.volatility
                )
                payoffs.append(self.get_initial_cost() - option_value)
            return np.array(payoffs)
    
    def get_initial_cost(self) -> float:
        # Negative cost = credit received
        return self.calculator.calculate_call_price(
            self.base_price, self.strike_price, self.time_to_expiration,
            self.risk_free_rate, self.volatility
        )

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

class SpreadStrategy(OptionStrategy):
    """Spread strategies (S1-S24)"""
    
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

class StrategyFactory:
    """Factory to create strategy objects from codes"""
    
    def __init__(self):
        self.strategies = self._initialize_strategies()
    
    def _initialize_strategies(self) -> Dict[str, StrategyConfig]:
        """Initialize all 84 strategy configurations"""
        strategies = {}
        
        # Long Call Strategies (C1-C15)
        moneyness_list = ["Deep OTM", "Deep OTM", "Deep OTM", "Shallow OTM", "Shallow OTM", 
                         "Shallow OTM", "ATM", "ATM", "ATM", "Shallow ITM", "Shallow ITM",
                         "Shallow ITM", "Deep ITM", "Deep ITM", "Deep ITM"]
        time_list = ["Near", "Medium", "Long"] * 5
        
        for i in range(15):
            code = f"C{i+1}"
            strategies[code] = StrategyConfig(
                code=code,
                name=f"Long Call - {moneyness_list[i]} - {time_list[i]}",
                strategy_type="call",
                moneyness=moneyness_list[i],
                time_frame=time_list[i],
                description=f"Buy {moneyness_list[i]} call option, {time_list[i]} expiration"
            )
        
        # Long Put Strategies (P1-P15)
        for i in range(15):
            code = f"P{i+1}"
            strategies[code] = StrategyConfig(
                code=code,
                name=f"Long Put - {moneyness_list[i]} - {time_list[i]}",
                strategy_type="put",
                moneyness=moneyness_list[i],
                time_frame=time_list[i],
                description=f"Buy {moneyness_list[i]} put option, {time_list[i]} expiration"
            )
        
        # Short Call Strategies (SC1-SC15)
        for i in range(15):
            code = f"SC{i+1}"
            strategies[code] = StrategyConfig(
                code=code,
                name=f"Short Call - {moneyness_list[i]} - {time_list[i]}",
                strategy_type="short_call",
                moneyness=moneyness_list[i],
                time_frame=time_list[i],
                description=f"Sell {moneyness_list[i]} call option, {time_list[i]} expiration"
            )
        
        # Short Put Strategies (SP1-SP15)
        for i in range(15):
            code = f"SP{i+1}"
            strategies[code] = StrategyConfig(
                code=code,
                name=f"Short Put - {moneyness_list[i]} - {time_list[i]}",
                strategy_type="short_put",
                moneyness=moneyness_list[i],
                time_frame=time_list[i],
                description=f"Sell {moneyness_list[i]} put option, {time_list[i]} expiration"
            )
        
        # Spread Strategies (S1-S24) - Simplified
        spread_names = [
            "Bull Call Spread", "Bull Call Spread", "Bull Call Spread",
            "Bear Call Spread", "Bear Call Spread", "Bear Call Spread",
            "Bull Put Spread", "Bull Put Spread", "Bull Put Spread",
            "Bear Put Spread", "Bear Put Spread", "Bear Put Spread",
            "Calendar Spread", "Calendar Spread", "Ratio Spread", "Ratio Spread",
            "Back Ratio Spread", "Back Ratio Spread", "Iron Condor", "Iron Condor",
            "Iron Condor", "Butterfly Spread", "Butterfly Spread", "Butterfly Spread"
        ]
        
        for i in range(24):
            code = f"S{i+1}"
            time_frame = time_list[i % 3] if i < 21 else time_list[i % 3]
            strategies[code] = StrategyConfig(
                code=code,
                name=spread_names[i] + f" - {time_frame}",
                strategy_type="spread",
                moneyness="Mixed",
                time_frame=time_frame,
                description=f"{spread_names[i]} strategy, {time_frame} expiration"
            )
        
        return strategies
    
    def create_strategy(self, code: str, base_price: float = 100.0) -> Optional[OptionStrategy]:
        """Create strategy object from code"""
        if code not in self.strategies:
            return None
        
        config = self.strategies[code]
        
        if config.strategy_type == "call":
            return LongCallStrategy(config, base_price)
        elif config.strategy_type == "put":
            return LongPutStrategy(config, base_price)
        elif config.strategy_type == "short_call":
            return ShortCallStrategy(config, base_price)
        elif config.strategy_type == "short_put":
            return ShortPutStrategy(config, base_price)
        elif config.strategy_type == "spread":
            # Check if it's an Iron Condor (S19, S20, S21)
            if code in ["S19", "S20", "S21"]:
                return IronCondorStrategy(config, base_price)
            else:
                return SpreadStrategy(config, base_price)
        
        return None
    
    def list_strategies(self) -> List[str]:
        """List all available strategy codes"""
        return sorted(self.strategies.keys())
    
    def get_strategy_info(self, code: str) -> Optional[StrategyConfig]:
        """Get strategy configuration info"""
        return self.strategies.get(code)

class VisualizationEngine:
    """Generate visualizations for options strategies"""
    
    def __init__(self, strategy: OptionStrategy, output_dir: str = 'strategy_plot'):
        self.strategy = strategy
        self.output_dir = output_dir
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_full_analysis(self, stock_range: Tuple[float, float] = (80, 120)):
        """Generate complete 4-panel analysis"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'{self.strategy.config.code}: {self.strategy.config.name}', 
                    fontsize=16, fontweight='bold')
        
        stock_prices = np.linspace(stock_range[0], stock_range[1], 100)
        
        # 1. Payoff at Expiration
        self._plot_expiration_payoff(ax1, stock_prices)
        
        # 2. Time Decay Effect
        self._plot_time_decay(ax2, stock_prices)
        
        # 3. Volatility Effect
        self._plot_volatility_effect(ax3, stock_prices)
        
        # 4. Strategy Summary
        self._plot_strategy_summary(ax4)
        
        plt.tight_layout()
        
        # Save plot to file
        filename = f"{self.strategy.config.code}_analysis.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"📊 Plot saved to: {filepath}")
        
        # Also try to show if in interactive environment
        try:
            plt.show()
        except:
            print("💡 Plot saved to file (interactive display not available)")
        
        # Print analysis
        self._print_analysis()
    
    def _plot_expiration_payoff(self, ax, stock_prices):
        """Plot payoff at expiration"""
        payoffs = self.strategy.calculate_payoff(stock_prices, 0)
        
        ax.plot(stock_prices, payoffs, 'b-', linewidth=2, label='Strategy Payoff')
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=self.strategy.base_price, color='gray', linestyle='--', alpha=0.5, label='Current Price')
        
        # Color profit/loss zones
        ax.fill_between(stock_prices, payoffs, 0, where=payoffs > 0, alpha=0.3, color='green', label='Profit')
        ax.fill_between(stock_prices, payoffs, 0, where=payoffs < 0, alpha=0.3, color='red', label='Loss')
        
        ax.set_xlabel('Stock Price at Expiration')
        ax.set_ylabel('Profit/Loss')
        ax.set_title('Payoff at Expiration')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_time_decay(self, ax, stock_prices):
        """Plot time decay effect"""
        time_scenarios = [
            self.strategy.time_to_expiration,
            self.strategy.time_to_expiration * 0.75,
            self.strategy.time_to_expiration * 0.5,
            self.strategy.time_to_expiration * 0.25,
            0
        ]
        colors = ['blue', 'green', 'orange', 'red', 'purple']
        
        for i, time_left in enumerate(time_scenarios):
            payoffs = self.strategy.calculate_payoff(stock_prices, time_left)
            label = f'{int(time_left*365)} days' if time_left > 0 else 'Expiration'
            ax.plot(stock_prices, payoffs, color=colors[i], linewidth=2, label=label)
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=self.strategy.base_price, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('Stock Price')
        ax.set_ylabel('Profit/Loss')
        ax.set_title('Time Decay Effect')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_volatility_effect(self, ax, stock_prices):
        """Plot volatility effect"""
        original_vol = self.strategy.volatility
        vol_scenarios = [0.15, 0.20, 0.25, 0.30, 0.40]
        
        for vol in vol_scenarios:
            self.strategy.volatility = vol
            payoffs = self.strategy.calculate_payoff(stock_prices, self.strategy.time_to_expiration)
            ax.plot(stock_prices, payoffs, linewidth=2, label=f'IV = {vol*100:.0f}%')
        
        # Restore original volatility
        self.strategy.volatility = original_vol
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=self.strategy.base_price, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('Stock Price')
        ax.set_ylabel('Profit/Loss')
        ax.set_title('Volatility Effect')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _is_credit_strategy(self) -> bool:
        """Determine if this is a credit strategy"""
        if "short" in self.strategy.config.strategy_type:
            return True
        elif self.strategy.config.strategy_type == "spread":
            return "Bull Put" in self.strategy.config.name or "Bear Call" in self.strategy.config.name
        return False
    
    def _plot_strategy_summary(self, ax):
        """Plot strategy summary info"""
        ax.axis('off')
        
        is_credit = self._is_credit_strategy()
        cost = self.strategy.get_initial_cost()
        
        info_text = f"""
Strategy: {self.strategy.config.code}
Name: {self.strategy.config.name}
Type: {self.strategy.config.strategy_type.title()}
Moneyness: {self.strategy.config.moneyness}
Time Frame: {self.strategy.config.time_frame}

Current Stock: ${self.strategy.base_price:.2f}
Strike Price: ${self.strategy.strike_price}
Time to Expiration: {self.strategy.time_to_expiration*365:.0f} days
Volatility: {self.strategy.volatility*100:.0f}%

Initial {"Credit" if is_credit else "Cost"}: ${abs(cost):.2f}
{"(Credit Received)" if is_credit else "(Debit Paid)"}
        """
        
        ax.text(0.05, 0.95, info_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.5))
    
    def _print_analysis(self):
        """Print detailed analysis"""
        cost = self.strategy.get_initial_cost()
        is_credit = self._is_credit_strategy()
        print(f"\n=== {self.strategy.config.code}: {self.strategy.config.name} ===")
        print(f"Description: {self.strategy.config.description}")
        print(f"Current Stock Price: ${self.strategy.base_price:.2f}")
        print(f"Strike Price: ${self.strategy.strike_price}")
        print(f"Initial {'Credit' if is_credit else 'Cost'}: ${abs(cost):.2f}")
        print(f"Time to Expiration: {self.strategy.time_to_expiration*365:.0f} days")
        print(f"Implied Volatility: {self.strategy.volatility*100:.0f}%")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Options Strategy Analyzer - All 84 Strategies')
    parser.add_argument('strategy', nargs='?', help='Strategy code (e.g., SP7, C1, S15)')
    parser.add_argument('--list', action='store_true', help='List all available strategies')
    parser.add_argument('--info', help='Get info about a specific strategy')
    parser.add_argument('--price', type=float, default=100.0, help='Base stock price (default: 100)')
    parser.add_argument('--output-dir', default='strategy_plot', help='Output directory for plots (default: strategy_plot)')
    
    args = parser.parse_args()
    
    factory = StrategyFactory()
    
    if args.list:
        print("Available Strategy Codes:")
        print("=" * 50)
        strategies = factory.list_strategies()
        for i, code in enumerate(strategies):
            info = factory.get_strategy_info(code)
            print(f"{code:>4}: {info.name}")
            if (i + 1) % 20 == 0:  # Break into sections
                print()
        return
    
    if args.info:
        info = factory.get_strategy_info(args.info)
        if info:
            print(f"Strategy {info.code}: {info.name}")
            print(f"Type: {info.strategy_type}")
            print(f"Moneyness: {info.moneyness}")
            print(f"Time Frame: {info.time_frame}")
            print(f"Description: {info.description}")
        else:
            print(f"Strategy {args.info} not found")
        return
    
    if not args.strategy:
        print("Please provide a strategy code or use --list to see available strategies")
        print("Example: python option_strategy_analyzer.py SP7")
        return
    
    # Create and analyze strategy
    strategy = factory.create_strategy(args.strategy.upper(), args.price)
    if not strategy:
        print(f"Strategy {args.strategy} not found. Use --list to see available strategies.")
        return
    
    # Generate visualization
    viz = VisualizationEngine(strategy, args.output_dir)
    viz.generate_full_analysis()

if __name__ == "__main__":
    main() 