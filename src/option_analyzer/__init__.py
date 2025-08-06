"""
Option Strategy Analyzer - Modular Implementation
Comprehensive analysis of all 84 option strategies
"""

from .models import StrategyConfig
from .pricing import BlackScholesCalculator
from .strategies import (
    OptionStrategy, LongCallStrategy, LongPutStrategy,
    ShortCallStrategy, ShortPutStrategy, SpreadStrategy, IronCondorStrategy
)
from .factory import StrategyFactory
from .visualization import VisualizationEngine
from .cli import main

__version__ = "2.0.0"

__all__ = [
    'StrategyConfig',
    'BlackScholesCalculator',
    'OptionStrategy',
    'LongCallStrategy',
    'LongPutStrategy', 
    'ShortCallStrategy',
    'ShortPutStrategy',
    'SpreadStrategy',
    'IronCondorStrategy',
    'StrategyFactory',
    'VisualizationEngine',
    'main'
]
