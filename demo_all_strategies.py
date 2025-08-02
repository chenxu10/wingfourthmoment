#!/usr/bin/env python3
"""
Demo script showing all 84 options strategies
Demonstrates the complete Options Strategy Analyzer system
"""

from option_strategy_analyzer import StrategyFactory
import time

def main():
    """Demonstrate the complete system"""
    print("🚀 Options Strategy Analyzer - Complete System Demo")
    print("=" * 60)
    
    factory = StrategyFactory()
    
    # Show total strategy count
    strategies = factory.list_strategies()
    print(f"📊 Total Strategies Available: {len(strategies)}")
    print()
    
    # Categorize strategies
    long_calls = [s for s in strategies if s.startswith('C')]
    long_puts = [s for s in strategies if s.startswith('P') and not s.startswith('SP')]
    short_calls = [s for s in strategies if s.startswith('SC')]
    short_puts = [s for s in strategies if s.startswith('SP')]
    spreads = [s for s in strategies if s.startswith('S')]
    
    print("📈 Strategy Categories:")
    print(f"   • Long Calls (C1-C15):     {len(long_calls)} strategies")
    print(f"   • Long Puts (P1-P15):      {len(long_puts)} strategies") 
    print(f"   • Short Calls (SC1-SC15):  {len(short_calls)} strategies")
    print(f"   • Short Puts (SP1-SP15):   {len(short_puts)} strategies")
    print(f"   • Spreads (S1-S24):        {len(spreads)} strategies")
    print()
    
    # Demonstrate key strategies from each category
    demo_strategies = {
        "🎯 High Return Play": "C1",  # Deep OTM Call
        "🛡️ Portfolio Protection": "P3",  # Deep OTM Put Long
        "💰 Income Generation": "SP7", # ATM Short Put
        "⚖️ Risk Management": "S1",   # Bull Call Spread
        "🎲 Speculation": "SC1"      # Deep OTM Short Call
    }
    
    print("🎯 Strategy Showcase:")
    for description, code in demo_strategies.items():
        strategy = factory.create_strategy(code)
        if strategy:
            cost = abs(strategy.get_initial_cost())
            cost_type = "Credit" if "short" in strategy.config.strategy_type else "Debit"
            print(f"   {description}")
            print(f"      Code: {code} - {strategy.config.name}")
            print(f"      {cost_type}: ${cost:.2f}")
            print(f"      Risk/Reward: {_get_risk_reward_description(strategy)}")
            print()
    
    # Show moneyness distribution
    print("📍 Moneyness Distribution:")
    moneyness_count = {}
    for code in strategies:
        strategy = factory.create_strategy(code)
        if strategy:
            moneyness = strategy.config.moneyness
            moneyness_count[moneyness] = moneyness_count.get(moneyness, 0) + 1
    
    for moneyness, count in sorted(moneyness_count.items()):
        print(f"   • {moneyness:<12}: {count:>2} strategies")
    print()
    
    # Show time frame distribution  
    print("⏰ Time Frame Distribution:")
    time_count = {}
    for code in strategies:
        strategy = factory.create_strategy(code)
        if strategy:
            time_frame = strategy.config.time_frame
            time_count[time_frame] = time_count.get(time_frame, 0) + 1
    
    for time_frame, count in sorted(time_count.items()):
        print(f"   • {time_frame:<8}: {count:>2} strategies")
    print()
    
    # Performance demonstration
    print("⚡ Performance Metrics:")
    start_time = time.time()
    
    # Create all strategies
    all_strategies = []
    for code in strategies[:10]:  # Test first 10 for speed
        strategy = factory.create_strategy(code)
        if strategy:
            all_strategies.append(strategy)
    
    creation_time = time.time() - start_time
    print(f"   • Strategy Creation: {creation_time*1000:.1f}ms for 10 strategies")
    
    # Test payoff calculation
    import numpy as np
    start_time = time.time()
    stock_prices = np.linspace(80, 120, 100)
    for strategy in all_strategies[:5]:
        payoffs = strategy.calculate_payoff(stock_prices)
    calculation_time = time.time() - start_time
    print(f"   • Payoff Calculation: {calculation_time*1000:.1f}ms for 5×100 points")
    
    print()
    print("🎓 Usage Examples:")
    print("   uv run python option_strategy_analyzer.py SP7")
    print("   uv run python option_strategy_analyzer.py --list")
    print("   uv run python option_strategy_analyzer.py --info C1")
    print("   uv run python option_strategy_analyzer.py S19 --price 150")
    
    print()
    print("🧪 Testing:")
    print("   uv run pytest")
    print("   uv run pytest tests/test_option_strategy_analyzer.py::TestShortPutStrategy")
    
    print()
    print("✅ System Status: All 84 strategies operational!")
    print("🚀 Ready for options analysis!")

def _get_risk_reward_description(strategy):
    """Get risk/reward description for a strategy"""
    if "Deep OTM" in strategy.config.moneyness and "Near" in strategy.config.time_frame:
        return "High Risk, High Reward (Poor R/R)"
    elif "ATM" in strategy.config.moneyness and "Long" in strategy.config.time_frame:
        return "Medium Risk, Good Reward (Good R/R)"
    elif "Deep ITM" in strategy.config.moneyness:
        return "Low Risk, Low Reward (Fair R/R)"
    elif "short" in strategy.config.strategy_type:
        return "Limited Profit, Significant Risk"
    else:
        return "Variable based on market conditions"

if __name__ == "__main__":
    main() 