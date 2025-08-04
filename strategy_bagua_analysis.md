# Options Strategy Bagua Analysis
## Comprehensive Analysis of All 84 Option Strategy Scenarios

### Legend:
- **Moneyness**: Deep OTM (Out-of-the-Money), Shallow OTM, ATM (At-the-Money), Shallow ITM (In-the-Money), Deep ITM
- **Time**: Near (0-30 days), Medium (30-90 days), Long (90+ days)
- **Cost**: L (Low), M (Medium), H (High), Credit (Net Credit)
- **Risk**: L (Low), M (Medium), H (High), U (Unlimited)
- **Leverage**: L (Low 1-3x), M (Medium 3-10x), H (High 10-50x), E (Extreme 50x+)
- **Risk/Reward**: E (Excellent), G (Good), F (Fair), P (Poor)

| Strategy | Moneyness | Type | Time | Cost | Risk | Max Profit | Leverage | Risk/Reward | Breakeven | Suitable Markets | Unsuitable Markets | Key Characteristics |
|----------|-----------|------|------|------|------|------------|----------|-------------|-----------|------------------|-------------------|-------------------|
| **CALL STRATEGIES** |
| C1 | Deep OTM | Call | Near | L | H | E (1000%+) | E | P | Strike + Premium | Strong Bull, News Catalyst, Regime Shift | Sideways, Bear, High IV, Stable Regime | Lottery ticket, extreme time decay |
| C2 | Deep OTM | Call | Medium | L-M | H | E (500-1000%) | H | F | Strike + Premium | Gradual Bull, Earnings Play, Vol Regime Change | Sideways, Bear, Vol Crush, Stable Regime | Better time cushion than near |
| C3 | Deep OTM | Call | Long | M | M-H | H (200-500%) | H | G | Strike + Premium | Long Bull Trend, Low IV, Structural Bull Regime | Range-bound, High IV, Bear Regime Shift | Time to be right, less decay |
| C4 | Shallow OTM | Call | Near | M | M-H | H (200-500%) | H | F | Strike + Premium | Strong Bull, Breakout, Momentum Regime | Sideways, Bear, Time Decay, Range Regime | Moderate probability play |
| C5 | Shallow OTM | Call | Medium | M | M | H (100-300%) | M-H | G | Strike + Premium | Steady Bull, Earnings, Growth Regime | Sideways, Vol Crush, Recession Regime | Balanced risk/reward |
| C6 | Shallow OTM | Call | Long | M-H | M | M-H (50-200%) | M | G | Strike + Premium | Bull Trend, Low IV Buy, Expansion Regime | Bear Market, High IV, Contraction Regime | Conservative growth play |
| C7 | ATM | Call | Near | M-H | M | M-H (100-200%) | M | F | Strike + Premium | Bull Momentum, Volatility, Trending Regime | Sideways, Time Decay, Range Regime | Delta ~0.5, high gamma |
| C8 | ATM | Call | Medium | H | M | M (50-150%) | M | G | Strike + Premium | Bull Trend, Vol Expansion, Growth Regime | Range-bound, Vol Crush, Stagnation Regime | Most liquid, balanced Greeks |
| C9 | ATM | Call | Long | H | L-M | M (30-100%) | L-M | G | Strike + Premium | Long Bull, Low IV, Secular Bull Regime | High IV, Mean Reversion, Bear Regime | Lower risk, steady gains |
| C10 | Shallow ITM | Call | Near | H | L-M | M (20-100%) | L-M | G | Strike + Premium | Bull Continuation, Momentum Regime | Sideways, High Decay, Range Regime | High delta, intrinsic value |
| C11 | Shallow ITM | Call | Medium | H | L | L-M (15-75%) | L-M | E | Strike + Premium | Steady Bull, Protection, Stable Bull Regime | Vol Crush, Reversal, Regime Shift | Good risk/reward balance |
| C12 | Shallow ITM | Call | Long | H | L | L-M (10-50%) | L | E | Strike + Premium | Conservative Bull, Long-term Bull Regime | High IV Purchase, Bear Regime Shift | Stock substitute, lower risk |
| C13 | Deep ITM | Call | Near | H | L | L (5-30%) | L | F | Strike + Premium | Bull Certainty, Income, Any Regime | Time Decay, Reversal, Major Regime Shift | High delta, low gamma |
| C14 | Deep ITM | Call | Medium | H | L | L (5-25%) | L | F | Strike + Premium | Steady Income, Bull, Stable Regime | Vol Crush, Range, Rate Regime Shift | Conservative income play |
| C15 | Deep ITM | Call | Long | H | L | L (3-20%) | L | F | Strike + Premium | Long Bull, Dividend Play, Any Regime | Opportunity Cost, Bear Regime Shift | Stock alternative, capital efficiency |
| **PUT STRATEGIES** |
| P1 | Deep OTM | Put | Near | L | H | E (1000%+) | E | P | Strike - Premium | Crash, Black Swan, Bear Regime Shift | Sideways, Bull, High IV, Stable Bull Regime | Crash protection, lottery |
| P2 | Deep OTM | Put | Medium | L-M | H | E (500-1000%) | H | F | Strike - Premium | Bear Market, Recession, Economic Regime Shift | Bull, Vol Crush, Growth Regime | Crash hedge, bear bet |
| P3 | Deep OTM | Put | Long | M | M-H | H (200-500%) | H | G | Strike - Premium | Long Bear, Market Top, Structural Bear Regime | Bull Trend, High IV, Bull Regime Shift | Portfolio insurance |
| P4 | Shallow OTM | Put | Near | M | M-H | H (200-500%) | H | F | Strike - Premium | Bear Break, Correction, Volatility Regime | Bull, Sideways, Low Vol Regime | Moderate bear play |
| P5 | Shallow OTM | Put | Medium | M | M | H (100-300%) | M-H | G | Strike - Premium | Bear Trend, Earnings Miss, Contraction Regime | Bull, Vol Crush, Expansion Regime | Balanced bear strategy |
| P6 | Shallow OTM | Put | Long | M-H | M | M-H (50-200%) | M | G | Strike - Premium | Long Bear, High IV, Secular Bear Regime | Bull Market, Low IV, Bull Regime | Conservative bear play |
| P7 | ATM | Put | Near | M-H | M | M-H (100-200%) | M | F | Strike - Premium | Bear Momentum, Vol, Trending Down Regime | Bull, Time Decay, Range Regime | Delta ~-0.5, high gamma |
| P8 | ATM | Put | Medium | H | M | M (50-150%) | M | G | Strike - Premium | Bear Trend, Protection, Defensive Regime | Bull, Vol Crush, Growth Regime | Liquid hedge, balanced |
| P9 | ATM | Put | Long | H | L-M | M (30-100%) | L-M | G | Strike - Premium | Long Bear, Insurance, Risk-Off Regime | Bull Trend, Low Vol, Risk-On Regime | Portfolio protection |
| P10 | Shallow ITM | Put | Near | H | L-M | M (20-100%) | L-M | G | Strike - Premium | Bear Continuation, Momentum Down Regime | Bull, High Decay, Range Regime | High delta, intrinsic |
| P11 | Shallow ITM | Put | Medium | H | L | L-M (15-75%) | L-M | E | Strike - Premium | Steady Bear, Hedge, Stable Bear Regime | Bull Trend, Vol Crush, Bull Regime Shift | Good hedge ratio |
| P12 | Shallow ITM | Put | Long | H | L | L-M (10-50%) | L | E | Strike - Premium | Conservative Bear, Long-term Bear Regime | Bull Market, Bull Regime Shift | Short stock alternative |
| P13 | Deep ITM | Put | Near | H | L | L (5-30%) | L | F | Strike - Premium | Bear Certainty, Any Regime | Bull, Time Decay, Major Bull Regime Shift | High delta, guaranteed |
| P14 | Deep ITM | Put | Medium | H | L | L (5-25%) | L | F | Strike - Premium | Income, Bear, Stable Regime | Bull Market, Rate Regime Shift | Conservative short |
| P15 | Deep ITM | Put | Long | H | L | L (3-20%) | L | F | Strike - Premium | Long Bear, Dividend, Any Regime | Opportunity Cost, Bull Regime Shift | Short alternative |
| **SHORT CALL STRATEGIES** |
| SC1 | Deep OTM | Short Call | Near | Credit | U | L (Premium) | E | F | Strike + Premium | Sideways, Bear, High IV, Range Regime | Strong Bull, News Catalyst, Low IV | Premium collection, extreme risk |
| SC2 | Deep OTM | Short Call | Medium | Credit | U | L-M (Premium) | H | F | Strike + Premium | Range-bound, Bear, High IV, Stable Regime | Gradual Bull, Vol Expansion, Breakout | Time decay benefit, unlimited risk |
| SC3 | Deep OTM | Short Call | Long | Credit | U | M (Premium) | H | F | Strike + Premium | Long Bear/Range, High IV, Bear Regime | Long Bull Trend, Bull Regime Shift | Slow time decay, major risk |
| SC4 | Shallow OTM | Short Call | Near | Credit | U | L-M (Premium) | H | F | Strike + Premium | Sideways, Bear, High IV, Range Regime | Strong Bull, Momentum, Low IV | Moderate risk, good premium |
| SC5 | Shallow OTM | Short Call | Medium | Credit | U | M (Premium) | M-H | F | Strike + Premium | Range-bound, Bear, High IV, Recession Regime | Steady Bull, Growth Regime, Earnings | Balanced premium collection |
| SC6 | Shallow OTM | Short Call | Long | Credit | U | M-H (Premium) | M | F | Strike + Premium | Long Bear/Range, High IV, Contraction Regime | Bull Trend, Expansion Regime, Low IV | Conservative premium, major risk |
| SC7 | ATM | Short Call | Near | Credit | U | M (Premium) | M | F | Strike + Premium | Sideways, Bear, High IV, Range Regime | Bull Momentum, Trending, Low IV | High gamma risk, good premium |
| SC8 | ATM | Short Call | Medium | Credit | U | M-H (Premium) | M | F | Strike + Premium | Range-bound, Bear, High IV, Stagnation Regime | Bull Trend, Growth Regime, Vol Expansion | Most liquid, balanced risk |
| SC9 | ATM | Short Call | Long | Credit | U | H (Premium) | L-M | G | Strike + Premium | Long Bear/Range, High IV, Bear Regime | Long Bull, Bull Regime, Low IV | Lower risk, steady income |
| SC10 | Shallow ITM | Short Call | Near | Credit | U | M-H (Premium) | L-M | F | Strike + Premium | Sideways, Bear, High IV, Range Regime | Bull Continuation, Momentum, Low IV | Assignment risk, intrinsic loss |
| SC11 | Shallow ITM | Short Call | Medium | Credit | U | H (Premium) | L-M | G | Strike + Premium | Range-bound, Bear, High IV, Bear Regime | Steady Bull, Bull Regime, Vol Expansion | Good income, assignment risk |
| SC12 | Shallow ITM | Short Call | Long | Credit | U | H (Premium) | L | E | Strike + Premium | Long Bear/Range, High IV, Bear Regime | Conservative Bull, Bull Regime Shift | High premium, covered call alternative |
| SC13 | Deep ITM | Short Call | Near | Credit | U | H (Premium) | L | G | Strike + Premium | Bear Certainty, High IV, Any Regime | Bull Certainty, Bull Regime, Low IV | Almost certain assignment |
| SC14 | Deep ITM | Short Call | Medium | Credit | U | H (Premium) | L | G | Strike + Premium | Bear Market, High IV, Bear Regime | Steady Bull, Bull Regime, Vol Expansion | High income, likely assignment |
| SC15 | Deep ITM | Short Call | Long | Credit | U | H (Premium) | L | E | Strike + Premium | Long Bear, High IV, Bear Regime | Long Bull, Bull Regime Shift, Low IV | Maximum premium, stock alternative |
| **SHORT PUT STRATEGIES** |
| SP1 | Deep OTM | Short Put | Near | Credit | L | L (Premium) | E | F | Strike - Premium | Bull, Sideways, High IV, Stable Bull Regime | Crash, Bear Regime Shift, Low IV | Premium collection, crash risk |
| SP2 | Deep OTM | Short Put | Medium | Credit | L | L-M (Premium) | H | F | Strike - Premium | Bull, Range-bound, High IV, Growth Regime | Bear Market, Recession, Vol Expansion | Time decay benefit, crash exposure |
| SP3 | Deep OTM | Short Put | Long | Credit | M | M (Premium) | H | F | Strike - Premium | Long Bull, High IV, Bull Regime | Long Bear, Bear Regime Shift, Low IV | Slow decay, portfolio risk |
| SP4 | Shallow OTM | Short Put | Near | Credit | M | L-M (Premium) | H | F | Strike - Premium | Bull, Sideways, High IV, Low Vol Regime | Bear Break, Volatility Regime, Low IV | Moderate risk, decent premium |
| SP5 | Shallow OTM | Short Put | Medium | Credit | M | M (Premium) | M-H | G | Strike - Premium | Bull, Range-bound, High IV, Expansion Regime | Bear Trend, Contraction Regime, Vol Expansion | Balanced strategy, assignment possible |
| SP6 | Shallow OTM | Short Put | Long | Credit | M | M-H (Premium) | M | G | Strike - Premium | Long Bull, High IV, Bull Regime | Long Bear, Bear Regime, Low IV | Conservative income, put assignment |
| SP7 | ATM | Short Put | Near | Credit | M | M (Premium) | M | F | Strike - Premium | Bull, Sideways, High IV, Range Regime | Bear Momentum, Trending Down, Low IV | High gamma risk, 50% assignment |
| SP8 | ATM | Short Put | Medium | Credit | M | M-H (Premium) | M | G | Strike - Premium | Bull, Range-bound, High IV, Growth Regime | Bear Trend, Defensive Regime, Vol Expansion | Liquid, balanced assignment risk |
| SP9 | ATM | Short Put | Long | Credit | L-M | H (Premium) | L-M | G | Strike - Premium | Long Bull, High IV, Risk-On Regime | Long Bear, Risk-Off Regime, Low IV | Lower assignment risk, income |
| SP10 | Shallow ITM | Short Put | Near | Credit | M | M-H (Premium) | L-M | F | Strike - Premium | Bull, Sideways, High IV, Range Regime | Bear Continuation, Momentum Down, Low IV | Likely assignment, intrinsic loss |
| SP11 | Shallow ITM | Short Put | Medium | Credit | L | H (Premium) | L-M | G | Strike - Premium | Bull, Range-bound, High IV, Bull Regime | Steady Bear, Bear Regime Shift, Vol Expansion | Good premium, assignment likely |
| SP12 | Shallow ITM | Short Put | Long | Credit | L | H (Premium) | L | E | Strike - Premium | Long Bull, High IV, Bull Regime | Conservative Bear, Bear Regime Shift, Low IV | High premium, cash-secured put |
| SP13 | Deep ITM | Short Put | Near | Credit | L | H (Premium) | L | G | Strike - Premium | Bull Certainty, High IV, Any Regime | Bear Certainty, Bear Regime, Low IV | Almost certain assignment |
| SP14 | Deep ITM | Short Put | Medium | Credit | L | H (Premium) | L | G | Strike - Premium | Bull Market, High IV, Bull Regime | Bear Market, Bear Regime, Vol Expansion | High income, assignment guaranteed |
| SP15 | Deep ITM | Short Put | Long | Credit | L | H (Premium) | L | E | Strike - Premium | Long Bull, High IV, Bull Regime | Long Bear, Bear Regime Shift, Low IV | Maximum premium, stock acquisition |
| **SPREAD STRATEGIES** |
| S1 | Mixed | Bull Call Spread | Near | M | L | L (50-200%) | M | G | Lower Strike + Premium | Moderate Bull, Defined Risk | Strong Bull, Bear, High IV | Limited upside, controlled risk |
| S2 | Mixed | Bull Call Spread | Medium | M-H | L | L-M (30-150%) | M | G | Lower Strike + Premium | Steady Bull, Earnings Play | Bear, Vol Crush, Range | Popular spread, liquid |
| S3 | Mixed | Bull Call Spread | Long | H | L | L-M (20-100%) | L-M | E | Lower Strike + Premium | Long Bull, Conservative | Bear Regime, High IV Buy | Low risk defined upside |
| S4 | Mixed | Bear Call Spread | Near | Credit | L | L (20-100%) | L-M | F | Upper Strike - Credit | Sideways, Bear, High IV | Strong Bull, Low IV | Income generation, time decay |
| S5 | Mixed | Bear Call Spread | Medium | Credit | L | L (15-75%) | L | F | Upper Strike - Credit | Range-bound, Bear | Bull Breakout, Vol Expansion | Consistent income strategy |
| S6 | Mixed | Bear Call Spread | Long | Credit | L | L (10-50%) | L | F | Upper Strike - Credit | Long-term Bear/Range | Bull Regime Shift | Conservative premium collection |
| S7 | Mixed | Bull Put Spread | Near | Credit | L | L (20-100%) | L-M | G | Higher Strike - Credit | Bull, High IV Sell | Bear Break, Low IV | Premium collection with upside |
| S8 | Mixed | Bull Put Spread | Medium | Credit | L | L-M (15-75%) | L | G | Higher Strike - Credit | Steady Bull, Vol Crush | Bear Trend, Vol Expansion | Income with bull bias |
| S9 | Mixed | Bull Put Spread | Long | Credit | L | L (10-50%) | L | E | Higher Strike - Credit | Long Bull, Premium Income | Bear Regime, Rate Shifts | Conservative bull income |
| S10 | Mixed | Bear Put Spread | Near | M | L | L (50-200%) | M | G | Higher Strike + Premium | Bear Break, Protection | Bull, High IV Purchase | Defined risk bear play |
| S11 | Mixed | Bear Put Spread | Medium | M-H | L | L-M (30-150%) | M | G | Higher Strike + Premium | Bear Trend, Hedge | Bull Market, Vol Crush | Portfolio protection |
| S12 | Mixed | Bear Put Spread | Long | H | L | L-M (20-100%) | L-M | E | Higher Strike + Premium | Long Bear, Insurance | Bull Regime, Opportunity Cost | Conservative bear hedge |
| S13 | ATM | Calendar Spread (Near/Medium) | Mixed | M | M | M (30-150%) | M | G | Complex Calculation | Low Vol, Time Decay | High Vol, Direction | Sell near, buy medium expiry |
| S14 | ATM | Calendar Spread (Near/Long) | Mixed | M-H | M | M-H (20-100%) | M | F | Complex Calculation | Stable Markets, Vol Crush | Trending, Vol Expansion | Sell near, buy long expiry |
| S15 | Mixed | Ratio Spread | Near | L-Credit | H | H-U (200%+) | H | F | Net Strike Calculation | Moderate Bull, Vol Sell | Strong Bull, Vol Expansion | Unlimited risk above breakeven |
| S16 | Mixed | Ratio Spread | Medium | L-Credit | H | H-U (100-300%) | H | F | Net Strike Calculation | Range-bound, High IV | Trending, Low IV | Complex risk profile |
| S17 | Mixed | Back Ratio Spread | Near | M-H | M-H | H-U (300%+) | H | F | Net Strike Calculation | High Vol, Direction | Low Vol, Range | Long volatility play |
| S18 | Mixed | Back Ratio Spread | Medium | H | M-H | H-U (200-500%) | H | G | Net Strike Calculation | Vol Expansion, Breakout | Vol Crush, Sideways | Advanced volatility strategy |
| S19 | Mixed | Iron Condor | Near | Credit | L | L (10-50%) | L-M | E | Middle Range | Range-bound, High IV | Trending, Low IV | Premium collection, range play |
| S20 | Mixed | Iron Condor | Medium | Credit | L | L-M (8-40%) | L | E | Middle Range | Sideways, Vol Crush | Breakout, Vol Expansion | Consistent income, neutral |
| S21 | Mixed | Iron Condor | Long | Credit | L | L (5-30%) | L | F | Middle Range | Long-term Range | Regime Shifts, Trends | Conservative range strategy |
| S22 | ATM | Butterfly Spread | Near | M | L | L (50-300%) | M | G | Middle Strike | Low Vol, Pin Risk | High Vol, Movement | Limited risk/reward |
| S23 | ATM | Butterfly Spread | Medium | M-H | L | L-M (30-200%) | M | G | Middle Strike | Range-bound, Vol Sell | Trending, Vol Buy | Classic neutral strategy |
| S24 | ATM | Butterfly Spread | Long | H | L | L (20-150%) | L-M | F | Middle Strike | Long-term Pin | Major Moves, Shifts | Conservative neutral play |

## Strategy Selection Matrix

### **High Probability Plays (>60% success rate):**
- Deep ITM Calls/Puts (All timeframes)
- Shallow ITM Medium/Long term
- ATM Long term

### **High Return Plays (>200% potential):**
- Deep OTM (All combinations)
- Shallow OTM Near/Medium term
- ATM Near term in trending markets

### **Risk Management Plays:**
- Deep ITM Long term (lowest risk)
- ATM Long term (balanced)
- Shallow ITM Medium term (moderate risk)

### **Market Condition Guidelines:**

**Strong Trending Markets:** OTM options in trend direction
**Volatile/Uncertain Markets:** ATM straddles/strangles
**Low Volatility Markets:** ITM options for steady gains
**High Volatility Markets:** Sell premium strategies
**Near Earnings/Events:** Avoid near-term unless directional conviction

### **Regime Shift Considerations:**

**Bull to Bear Regime Shift:**
- Deep OTM puts become highly attractive (P1-P3)
- Exit all call positions except deep ITM
- Focus on portfolio protection strategies
- Volatility typically spikes during transition

**Bear to Bull Regime Shift:**
- Deep OTM calls offer explosive potential (C1-C3)
- Exit put positions except as insurance
- ITM calls provide safer transition plays
- Watch for false breakouts during early stages

**Low to High Volatility Regime:**
- Sell premium strategies become profitable
- Avoid buying expensive options
- Focus on time decay strategies
- ATM straddles/strangles for volatility plays

**High to Low Volatility Regime:**
- Buy cheap options before vol collapses
- Exit short premium positions
- Focus on directional plays
- ITM options provide stability

**Interest Rate Regime Shifts:**
- Rising rates: Favor calls over puts (growth stocks suffer)
- Falling rates: Favor growth stock calls
- Rate volatility increases option premiums
- Consider duration impact on underlying assets

**Economic Expansion to Contraction:**
- Defensive sectors outperform
- Put spreads on cyclical stocks
- Long-term protective puts essential
- Focus on quality companies with ITM options

**Market Structure Regime Changes:**
- Algorithmic trading increases: Higher gamma risk
- Liquidity regime changes: Impact bid-ask spreads
- Correlation regime shifts: Sector rotation strategies
- Central bank policy changes: Systematic volatility patterns

### **Key Risk Factors:**
1. **Time Decay (Theta):** Most severe in near-term OTM
2. **Volatility Crush:** After earnings/events
3. **Gap Risk:** Overnight moves against position
4. **Liquidity Risk:** Deep OTM/ITM options
5. **Assignment Risk:** ITM short options near expiration

---

## Market Condition Catalog
### **Extracted from All Strategy Analysis**

### **SUITABLE MARKET CONDITIONS:**

**Bullish Conditions:**
- Strong Bull
- Gradual Bull  
- Long Bull Trend
- Bull Momentum
- Bull Trend
- Bull Continuation
- Steady Bull
- Conservative Bull
- Bull Certainty
- Moderate Bull
- Long Bull
- Secular Bull Regime
- Structural Bull Regime
- Growth Regime
- Expansion Regime
- Stable Bull Regime
- Long-term Bull Regime
- Momentum Regime
- Trending Regime

**Bearish Conditions:**
- Bear Market
- Long Bear
- Bear Break
- Bear Trend
- Bear Momentum
- Bear Continuation
- Steady Bear
- Conservative Bear
- Bear Certainty
- Long-term Bear Regime
- Structural Bear Regime
- Bear Regime Shift
- Economic Regime Shift
- Contraction Regime
- Defensive Regime
- Risk-Off Regime
- Secular Bear Regime
- Trending Down Regime
- Stable Bear Regime

**Neutral/Range Conditions:**
- Sideways
- Range-bound
- Long-term Range
- Any Regime
- Stable Regime

**Volatility Conditions:**
- High IV
- Low IV
- Vol Expansion
- Vol Crush
- High Vol
- Low Vol
- Volatility Regime

**Event-Driven Conditions:**
- News Catalyst
- Earnings Play
- Earnings
- Earnings Miss
- Breakout
- Crash
- Black Swan
- Market Top
- Correction
- Regime Shift
- Vol Regime Change

**Specialized Conditions:**
- Time Decay
- Pin Risk
- Defined Risk
- Protection
- Hedge
- Insurance
- Income
- Dividend Play
- Premium Income

### **UNSUITABLE MARKET CONDITIONS:**

**Conflicting Directional Bias:**
- Bull (for bear strategies)
- Bear (for bull strategies)
- Strong Bull (for bear/neutral strategies)
- Bull Market (for bear strategies)
- Bull Trend (for bear strategies)
- Bull Breakout (for bear/range strategies)
- Bull Continuation (for bear strategies)

**Volatility Mismatches:**
- High IV (when buying options)
- Low IV (when selling premium)
- Vol Crush (for long option strategies)
- Vol Expansion (for short premium strategies)

**Time Decay Issues:**
- Time Decay (for long options near expiry)
- High Decay (for short-term long positions)

**Range vs Trending Conflicts:**
- Sideways (for directional strategies)
- Range-bound (for trending strategies)
- Trending (for range strategies)
- Range Regime (for momentum strategies)

**Regime Shift Risks:**
- Regime Shift (for stable strategies)
- Bear Regime Shift (for bull strategies)
- Bull Regime Shift (for bear strategies)
- Major Regime Shift (for any single direction)
- Rate Regime Shift (for rate-sensitive strategies)

**Opportunity Cost Scenarios:**
- Opportunity Cost (for conservative strategies)
- Major Moves (for neutral strategies)
- Breakout (for range strategies)
- High Vol Movement (for low vol strategies)

**Stability vs Volatility Conflicts:**
- Stable Regime (for volatility plays)
- Stagnation Regime (for growth strategies)
- Low Vol Regime (for volatility strategies)
- Growth Regime (for bear strategies)
- Risk-On Regime (for defensive strategies)

### **MARKET CONDITION USAGE GUIDE:**

**For Strategy Selection:**
1. **Identify Current Market Regime** from the suitable conditions list
2. **Avoid Strategies** that list current conditions as unsuitable
3. **Cross-reference** volatility environment with strategy requirements
4. **Consider Time Horizon** alignment with market outlook
5. **Monitor for Regime Changes** that could shift suitability

**Red Flag Combinations:**
- High IV + Long Options = Expensive entry
- Low IV + Short Premium = Limited income potential  
- Time Decay + Long Near-Term = Rapid value erosion
- Regime Shift + Single Direction = High reversal risk
- Trending + Range Strategy = Poor fit 