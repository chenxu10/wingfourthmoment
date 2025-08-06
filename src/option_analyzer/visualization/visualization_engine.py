"""
Visualization engine for option strategies
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

from ..strategies import OptionStrategy


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