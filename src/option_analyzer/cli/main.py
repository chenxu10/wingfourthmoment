"""
Command line interface for option strategy analyzer
"""

import argparse

from ..factory import StrategyFactory
from ..visualization import VisualizationEngine


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