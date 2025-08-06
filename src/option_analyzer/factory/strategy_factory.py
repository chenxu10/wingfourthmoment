"""
Strategy factory for creating option strategy instances
"""

from typing import Dict, List, Optional

from ..models import StrategyConfig
from ..strategies import (
    OptionStrategy, LongCallStrategy, LongPutStrategy,
    ShortCallStrategy, ShortPutStrategy, SpreadStrategy, IronCondorStrategy
)


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