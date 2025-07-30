# Wing Fourth Moment - NDX100 Options Delta Hedging Calculator

## Problem Statement

Trading NDX100 through QQQ and TQQQ options presents a unique mathematical challenge when trying to maintain delta neutrality across different leverage ratios. This tool solves the complex problem of calculating optimal hedge ratios when selling near-the-money options on one instrument while hedging with far out-of-the-money options on another.

## The Trading Strategy

Many professional options traders employ the following strategy on NDX100:

1. **Primary Position**: Sell weekly options on TQQQ (3x leveraged NDX100 ETF) that are close to at-the-money
   - Target: Options with less than 3% move from current underlying price
   - Collect premium from time decay on high-probability trades
   - Examples: Selling TQQQ $45 calls when TQQQ trades at $44, or selling $43 puts

2. **Hedge Requirement**: Maintain delta neutrality to protect against directional moves
   - Challenge: Direct hedging with TQQQ options is expensive due to high implied volatility
   - Solution: Use far out-of-the-money QQQ options (1x NDX100 ETF) as cheaper hedges

3. **The Mathematical Problem**: Calculate the correct number of QQQ hedge contracts needed
   - Both QQQ and TQQQ track NDX100, but with different leverage ratios (1x vs 3x)
   - Option deltas behave differently due to different underlying prices and volatilities
   - Strike price relationships are non-linear due to leverage effects

## How Traders Can Use This Tool

### Input Parameters
- **TQQQ Position**: Your current short options position (calls/puts, strike, expiration, quantity)
- **Market Data**: Current QQQ and TQQQ prices, implied volatilities, interest rates
- **Hedge Preferences**: Desired QQQ option expiration and approximate delta range for hedge options

### Output Calculations
- **Optimal Hedge Ratio**: Exact number of QQQ contracts needed per TQQQ contract sold
- **Delta Sensitivity Analysis**: How hedge ratios change with underlying price movements
- **Cost Analysis**: Compare hedging costs between different QQQ strike prices and expirations
- **Risk Metrics**: Gamma, theta, and vega exposures of the combined position

### Typical Use Cases

#### Case 1: Weekly TQQQ Call Sales
```
Position: Short 10 TQQQ $45 calls (TQQQ trading at $44.50)
Hedge: Buy ? QQQ $380 calls (QQQ trading at $370)
Tool Output: Buy 12 QQQ calls for approximate delta neutrality
```

#### Case 2: TQQQ Strangle Strategy
```
Position: Short TQQQ $44 puts and $46 calls (TQQQ at $45)
Hedge: Combination of far OTM QQQ puts and calls
Tool Output: Optimal strike selection and quantities for both sides
```

#### Case 3: Rolling Hedge Positions
```
Scenario: TQQQ moves from $45 to $47, existing hedge is now inadequate
Tool Output: Adjustment recommendations for maintaining delta neutrality
```

## The Mathematical Challenge

### Leverage Transformation
The core complexity lies in translating between 1x and 3x leveraged instruments:

- **Price Relationship**: TQQQ ≈ (QQQ/QQQ₀)³ × TQQQ₀ (approximately, with daily rebalancing effects)
- **Delta Relationship**: Δ_TQQQ ≈ 3 × Δ_QQQ × (price adjustment factors)
- **Volatility Scaling**: TQQQ implied volatility ≈ QQQ implied volatility × leverage factor

### Options Greeks Complexity
Each Greek requires different transformation mathematics:
- **Delta**: Linear leverage scaling with adjustment factors
- **Gamma**: Non-linear scaling due to second-order effects
- **Theta**: Time decay interactions with leverage
- **Vega**: Volatility sensitivity changes with leverage ratios

### Market Microstructure Considerations
- **Bid-Ask Spreads**: Different liquidity profiles between QQQ and TQQQ options
- **Volatility Skew**: Different implied volatility curves
- **Dividend Adjustments**: QQQ receives dividends, TQQQ structure is different
- **Rebalancing Effects**: Daily rebalancing in leveraged ETFs affects long-term relationships

## Why This Tool Is Needed

### Current Market Gap
1. **No Existing Solutions**: Standard options calculators don't handle cross-instrument leverage relationships
2. **Manual Calculations Are Error-Prone**: Complex mathematics lead to hedging mistakes
3. **Dynamic Adjustment Needs**: Positions need frequent rebalancing as markets move

### Value Proposition
- **Precision**: Mathematically rigorous hedge ratio calculations
- **Speed**: Real-time calculations for fast-moving options markets
- **Risk Management**: Comprehensive Greeks analysis for portfolio-level risk control
- **Cost Optimization**: Find the most cost-effective hedge structures

## Target Users

- **Professional Options Traders**: Managing large NDX100 options portfolios
- **Quantitative Analysts**: Building systematic options strategies
- **Risk Managers**: Monitoring and controlling options portfolio risk
- **Individual Traders**: Sophisticated retail traders using QQQ/TQQQ strategies

## Getting Started

### Installation
```bash
pip install -r requirements.txt
```

### Quick Usage

The calculator is ready to use! Here are practical examples:

#### Example 1: Hedging Short TQQQ Calls
```bash
python3 hedge_calculator_cli.py \
  --tqqq-price 45.0 --tqqq-strike 46.0 --tqqq-quantity -10 --tqqq-type call \
  --expiry 2024-12-20 --qqq-price 370.0 --qqq-strike 380.0 --qqq-type call
```
**Result**: Buy 218 QQQ $380 calls to hedge 10 short TQQQ $46 calls

#### Example 2: Hedging Short TQQQ Puts  
```bash
python3 hedge_calculator_cli.py \
  --tqqq-price 45.0 --tqqq-strike 44.0 --tqqq-quantity -5 --tqqq-type put \
  --expiry 2024-12-27 --qqq-price 370.0 --qqq-strike 360.0 --qqq-type put
```
**Result**: Buy 128 QQQ $360 puts to hedge 5 short TQQQ $44 puts

### Command Line Parameters
- `--tqqq-price`: Current TQQQ market price
- `--tqqq-strike`: Your TQQQ option strike price  
- `--tqqq-quantity`: Number of contracts (negative for short positions)
- `--tqqq-type`: call or put
- `--qqq-price`: Current QQQ market price
- `--qqq-strike`: QQQ hedge option strike price
- `--qqq-type`: call or put (typically same as TQQQ type)
- `--expiry`: Expiration date (YYYY-MM-DD format)
- `--volatility`: Implied volatility (optional, default 0.25)
- `--risk-free-rate`: Risk-free rate (optional, default 0.05)

---

*Disclaimer: This tool is for educational and analytical purposes. Options trading involves substantial risk and is not suitable for all investors. Always consult with qualified financial professionals before implementing complex options strategies.* 