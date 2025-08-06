# Options Strategy Analyzer - All 84 Strategies

A comprehensive Python tool for analyzing all 84 options strategies from the Options Strategy Bagua Analysis.

## Features

- **Complete Coverage**: All 84 strategies (C1-C15, P1-P15, SC1-SC15, SP1-SP15, S1-S24)
- **Interactive CLI**: Input strategy codes and get instant analysis
- **4-Panel Visualization**: Expiration payoff, time decay, volatility effects, strategy summary
- **Accurate Pricing**: Black-Scholes calculations with Greeks
- **Unit Tests**: Comprehensive test suite covering all functionality

## Quick Start

### 1. List All Available Strategies
```bash
uv run python option_strategy_analyzer.py --list
```

### 2. Get Strategy Information
```bash
uv run python option_strategy_analyzer.py --info SP7
```

### 3. Analyze a Strategy (Generate Charts)
```bash
uv run python option_strategy_analyzer.py SP7
```

### 4. Custom Stock Price
```bash
uv run python option_strategy_analyzer.py SP7 --price 150
```

### 5. Save Plots to Custom Directory
```bash
uv run python option_strategy_analyzer.py SP7 --output-dir ./plots
```

### Alternative (without uv)
```bash
python3 option_strategy_analyzer.py SP7
```

## Strategy Codes Reference

### Long Options (Buy)
- **C1-C15**: Long Calls (Deep OTM → Deep ITM, Near → Long term)
- **P1-P15**: Long Puts (Deep OTM → Deep ITM, Near → Long term)

### Short Options (Sell)
- **SC1-SC15**: Short Calls (Deep OTM → Deep ITM, Near → Long term)
- **SP1-SP15**: Short Puts (Deep OTM → Deep ITM, Near → Long term)

### Spreads
- **S1-S24**: Various spread strategies (Bull/Bear, Call/Put, Calendar, etc.)

## Example Usage

### SP7 Analysis (ATM Short Put, Near Term)
```bash
uv run python option_strategy_analyzer.py SP7
```

**Expected Output:**
- Current Stock Price: $100.00
- Strike Price: $100.00 (ATM)
- Initial Credit: ~$2.65
- Breakeven: ~$97.35
- Max Profit: Premium received
- Max Loss: Strike - Premium (if stock → 0)

📊 **Plot Output**: Automatically saves comprehensive 4-panel analysis as `SP7_analysis.png` including:
- Payoff at Expiration diagram
- Time Decay Effect analysis  
- Volatility Sensitivity charts
- Strategy Summary with Greeks

### Key Strategy Examples

#### High Return Plays
```bash
uv run python option_strategy_analyzer.py C1   # Deep OTM Call (lottery ticket)
uv run python option_strategy_analyzer.py P1   # Deep OTM Put (crash protection)
```

#### Conservative Income
```bash
uv run python option_strategy_analyzer.py SP9   # Long-term Short Put
uv run python option_strategy_analyzer.py SC13  # Deep ITM Short Call
```

#### Spread Strategies
```bash
uv run python option_strategy_analyzer.py S1    # Bull Call Spread
uv run python option_strategy_analyzer.py S19   # Iron Condor
```

## Visualization Features

Each analysis generates 4 charts:

1. **Payoff at Expiration**: Classic options payoff diagram
2. **Time Decay Effect**: How position changes over time
3. **Volatility Effect**: Impact of IV changes
4. **Strategy Summary**: Key parameters and metrics

## Strategy Categories

### By Risk/Reward Profile
- **Excellent (E)**: Shallow/Deep ITM medium/long-term
- **Good (G)**: ATM and OTM long-term strategies  
- **Fair (F)**: Most near-term and complex strategies
- **Poor (P)**: Deep OTM near-term "lottery tickets"

### By Market Bias
- **Bullish**: C1-C15, SP1-SP15, Bull spreads
- **Bearish**: P1-P15, SC1-SC15, Bear spreads
- **Neutral**: ATM short strategies, Iron Condors, Butterflies

## Testing

Run the comprehensive test suite:

```bash
# Run all tests with uv
uv run pytest
```
### Test Coverage
- Black-Scholes calculations
- Strategy factory functionality
- All strategy types (calls, puts, shorts, spreads)
- Payoff calculations
- Error handling
- CLI interface
- Integration tests

## Advanced Usage

### Custom Parameters
```python
from option_strategy_analyzer import StrategyFactory, VisualizationEngine

factory = StrategyFactory()
strategy = factory.create_strategy("SP7", base_price=120.0)

# Modify parameters
strategy.volatility = 0.30  # 30% IV
strategy.risk_free_rate = 0.03  # 3% rate

# Generate analysis
viz = VisualizationEngine(strategy)
viz.generate_full_analysis()
```

### Batch Analysis
```python
strategies_to_analyze = ["SP7", "C7", "P7", "S1"]
for code in strategies_to_analyze:
    strategy = factory.create_strategy(code)
    if strategy:
        viz = VisualizationEngine(strategy)
        viz.generate_full_analysis()
```

## Setup with uv

### Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install dependencies
```bash
# Install core dependencies
uv sync

# Install with development dependencies
uv sync --extra dev

# Install with test dependencies  
uv sync --extra test
```

### Verify Setup
```bash
# Run verification script to check everything is working
python3 verify_setup.py
```

## File Structure

```
├── option_strategy_analyzer.py      # Main analyzer with CLI
├── tests/                           # Test directory
│   ├── __init__.py                  # Tests package init
│   ├── test_option_strategy_analyzer.py # Comprehensive unit tests
│   └── test_delta_calculator.py     # Delta calculator tests
├── short_put_payoff_analysis.py     # Original SP7 example
├── demo_all_strategies.py           # System demonstration
├── verify_setup.py                  # Setup verification script
├── strategy_bagua_analysis.md       # Complete strategy reference
├── pyproject.toml                   # uv configuration and dependencies
├── .gitignore                       # Git ignore file
└── README_strategy_analyzer.md      # This file
```

## Implementation Details

### Class Hierarchy
- `OptionStrategy` (Abstract base)
  - `LongCallStrategy`
  - `LongPutStrategy` 
  - `ShortCallStrategy`
  - `ShortPutStrategy`
  - `SpreadStrategy`

### Key Components
- `BlackScholesCalculator`: Accurate option pricing
- `StrategyFactory`: Creates strategies from codes
- `VisualizationEngine`: Generates 4-panel analysis
- `StrategyConfig`: Strategy metadata and configuration

### Moneyness Mapping
- **Deep OTM**: 10% away from current price
- **Shallow OTM**: 5% away from current price
- **ATM**: At current price
- **Shallow ITM**: 5% favorable
- **Deep ITM**: 10% favorable

### Time Frame Mapping
- **Near**: 30 days to expiration
- **Medium**: 60 days to expiration
- **Long**: 120 days to expiration

## Performance

- **Strategy Creation**: <1ms per strategy
- **Payoff Calculation**: <10ms for 100 price points
- **Visualization**: 2-3 seconds for complete 4-panel analysis
- **All 84 Strategies**: Can analyze entire suite in <5 minutes

## Error Handling

The system gracefully handles:
- Invalid strategy codes
- Extreme parameter values
- Zero time to expiration
- Mathematical edge cases
- Missing dependencies

## Contributing

1. Add new strategy types in `OptionStrategy` subclasses
2. Extend test coverage in `test_option_strategy_analyzer.py`
3. Update strategy mappings in `StrategyFactory`
4. Enhance visualizations in `VisualizationEngine`

## License

MIT License - Free for educational and commercial use.

---

**Quick Example**: `python3 option_strategy_analyzer.py SP7` generates complete analysis of ATM Short Put strategy! 