"""
Strategy configuration data model
"""

from dataclasses import dataclass


@dataclass
class StrategyConfig:
    """Configuration for an options strategy"""
    code: str
    name: str
    strategy_type: str  # call, put, short_call, short_put, spread
    moneyness: str     # Deep OTM, Shallow OTM, ATM, Shallow ITM, Deep ITM
    time_frame: str    # Near, Medium, Long
    description: str 