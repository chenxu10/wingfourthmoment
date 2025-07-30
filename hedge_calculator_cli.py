#!/usr/bin/env python3

"""
TQQQ/QQQ Delta Hedging Calculator
Command-line interface for calculating optimal QQQ hedge quantities
"""

import argparse
import sys
from datetime import datetime, timedelta
from delta_calculator import OptionCalculator


def calculate_time_to_expiry(expiry_date_str):
    """Convert expiry date string to time in years"""
    try:
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
        today = datetime.now()
        days_to_expiry = (expiry_date - today).days
        return max(days_to_expiry / 365.0, 0.001)  # Minimum 0.1% of year
    except ValueError:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD, got: {expiry_date_str}")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate QQQ hedge quantities for TQQQ options positions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Short 10 TQQQ $46 calls expiring 2024-03-15, TQQQ at $45, hedge with QQQ $380 calls
  python3 hedge_calculator_cli.py --tqqq-price 45.0 --tqqq-strike 46.0 --tqqq-quantity -10 
                                  --tqqq-type call --expiry 2024-03-15 --qqq-price 370.0 
                                  --qqq-strike 380.0 --qqq-type call

  # Short 5 TQQQ $44 puts, hedge with QQQ $360 puts
  python3 hedge_calculator_cli.py --tqqq-price 45.0 --tqqq-strike 44.0 --tqqq-quantity -5 
                                  --tqqq-type put --expiry 2024-03-15 --qqq-price 370.0 
                                  --qqq-strike 360.0 --qqq-type put
        """)
    
    # TQQQ position parameters
    parser.add_argument('--tqqq-price', type=float, required=True,
                       help='Current TQQQ market price')
    parser.add_argument('--tqqq-strike', type=float, required=True,
                       help='TQQQ option strike price')
    parser.add_argument('--tqqq-quantity', type=int, required=True,
                       help='TQQQ option quantity (negative for short positions)')
    parser.add_argument('--tqqq-type', choices=['call', 'put'], required=True,
                       help='TQQQ option type')
    
    # QQQ hedge parameters
    parser.add_argument('--qqq-price', type=float, required=True,
                       help='Current QQQ market price')
    parser.add_argument('--qqq-strike', type=float, required=True,
                       help='QQQ hedge option strike price')
    parser.add_argument('--qqq-type', choices=['call', 'put'], required=True,
                       help='QQQ hedge option type')
    
    # Common parameters
    parser.add_argument('--expiry', required=True,
                       help='Option expiration date (YYYY-MM-DD)')
    parser.add_argument('--risk-free-rate', type=float, default=0.05,
                       help='Risk-free interest rate (default: 0.05)')
    parser.add_argument('--volatility', type=float, default=0.25,
                       help='Implied volatility (default: 0.25)')
    
    args = parser.parse_args()
    
    try:
        # Calculate time to expiry
        time_to_expiry = calculate_time_to_expiry(args.expiry)
        
        # Create calculator and compute hedge
        calculator = OptionCalculator()
        
        hedge_quantity = calculator.calculate_hedge_quantity(
            tqqq_price=args.tqqq_price,
            tqqq_strike=args.tqqq_strike,
            tqqq_quantity=args.tqqq_quantity,
            tqqq_option_type=args.tqqq_type,
            qqq_price=args.qqq_price,
            qqq_strike=args.qqq_strike,
            qqq_option_type=args.qqq_type,
            time_to_expiry=time_to_expiry,
            risk_free_rate=args.risk_free_rate,
            volatility=args.volatility
        )
        
        # Display results
        print("\n" + "="*60)
        print("TQQQ/QQQ DELTA HEDGING CALCULATOR")
        print("="*60)
        
        print(f"\nTQQQ Position:")
        print(f"  Type: {args.tqqq_type.upper()}")
        print(f"  Strike: ${args.tqqq_strike:.2f}")
        print(f"  Quantity: {args.tqqq_quantity:,}")
        print(f"  Current Price: ${args.tqqq_price:.2f}")
        
        print(f"\nQQQ Hedge Option:")
        print(f"  Type: {args.qqq_type.upper()}")
        print(f"  Strike: ${args.qqq_strike:.2f}")
        print(f"  Current Price: ${args.qqq_price:.2f}")
        
        print(f"\nExpiration: {args.expiry}")
        print(f"Time to Expiry: {time_to_expiry:.4f} years ({time_to_expiry*365:.1f} days)")
        
        print(f"\n" + "-"*60)
        print("HEDGE RECOMMENDATION:")
        print("-"*60)
        
        if hedge_quantity > 0:
            action = "BUY"
        else:
            action = "SELL"
            
        print(f"\n{action} {abs(hedge_quantity):.0f} QQQ ${args.qqq_strike:.2f} {args.qqq_type}s")
        print(f"  (Exact quantity: {hedge_quantity:.2f})")
        
        if abs(hedge_quantity) < 0.1:
            print("\n⚠️  Warning: Very small hedge quantity - position may already be nearly delta neutral")
        
        print(f"\nThis hedge should approximately neutralize the delta risk from your")
        print(f"TQQQ {args.tqqq_type} position, accounting for the 3:1 leverage difference.")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 