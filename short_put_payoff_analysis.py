import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math

class BlackScholesCalculator:
    """Black-Scholes option pricing calculator"""
    
    def calculate_put_price(self, S, K, T, r, sigma):
        """Calculate put option price using Black-Scholes formula"""
        if T <= 0:
            return max(K - S, 0)
        
        d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
        d2 = d1 - sigma*math.sqrt(T)
        
        put_price = K*math.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
        return max(put_price, 0)

def short_put_payoff_analysis():
    """Analyze SP7: ATM Short Put Near Term strategy"""
    
    # Strategy parameters (SP7 from table)
    current_stock_price = 100.0
    strike_price = 100.0  # ATM
    risk_free_rate = 0.05
    initial_volatility = 0.25  # 25% IV
    days_to_expiration = 30  # Near term
    
    calculator = BlackScholesCalculator()
    
    # Calculate initial premium received
    initial_time = days_to_expiration / 365
    initial_premium = calculator.calculate_put_price(
        current_stock_price, strike_price, initial_time, risk_free_rate, initial_volatility
    )
    
    print(f"=== SP7: ATM Short Put Analysis ===")
    print(f"Strike Price: ${strike_price}")
    print(f"Current Stock: ${current_stock_price}")
    print(f"Initial Premium Received: ${initial_premium:.2f}")
    print(f"Breakeven Point: ${strike_price - initial_premium:.2f}")
    print(f"Max Profit: ${initial_premium:.2f}")
    print(f"Max Loss: ${strike_price - initial_premium:.2f} (if stock goes to 0)")
    
    # Create stock price range for analysis
    stock_range = np.linspace(80, 120, 100)
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('SP7: ATM Short Put Payoff Analysis', fontsize=16, fontweight='bold')
    
    # 1. Basic Payoff at Expiration
    expiration_payoff = []
    for S in stock_range:
        intrinsic_value = max(strike_price - S, 0)  # What we pay out
        net_payoff = initial_premium - intrinsic_value  # What we keep
        expiration_payoff.append(net_payoff)
    
    ax1.plot(stock_range, expiration_payoff, 'b-', linewidth=2, label='Short Put Payoff')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.axvline(x=strike_price, color='red', linestyle='--', alpha=0.5, label='Strike Price')
    ax1.axvline(x=strike_price - initial_premium, color='orange', linestyle='--', alpha=0.5, label='Breakeven')
    ax1.fill_between(stock_range, expiration_payoff, 0, where=np.array(expiration_payoff) > 0, alpha=0.3, color='green', label='Profit Zone')
    ax1.fill_between(stock_range, expiration_payoff, 0, where=np.array(expiration_payoff) < 0, alpha=0.3, color='red', label='Loss Zone')
    ax1.set_xlabel('Stock Price at Expiration')
    ax1.set_ylabel('Profit/Loss')
    ax1.set_title('Payoff at Expiration')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Time Decay Effect (Different days to expiration)
    time_scenarios = [30, 21, 14, 7, 3, 1]  # Days to expiration
    colors = ['blue', 'green', 'orange', 'red', 'purple', 'brown']
    
    for i, days in enumerate(time_scenarios):
        time_to_exp = max(days / 365, 0.001)  # Avoid zero
        payoffs = []
        
        for S in stock_range:
            if days == 0:  # At expiration
                option_value = max(strike_price - S, 0)
            else:
                option_value = calculator.calculate_put_price(
                    S, strike_price, time_to_exp, risk_free_rate, initial_volatility
                )
            net_payoff = initial_premium - option_value
            payoffs.append(net_payoff)
        
        ax2.plot(stock_range, payoffs, color=colors[i], linewidth=2, 
                label=f'{days} days to exp' if days > 0 else 'Expiration')
    
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.axvline(x=strike_price, color='red', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Stock Price')
    ax2.set_ylabel('Profit/Loss')
    ax2.set_title('Time Decay Effect (Theta)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Volatility Effect (Different IV levels)
    vol_scenarios = [0.15, 0.20, 0.25, 0.30, 0.40, 0.50]  # Different volatilities
    
    for i, vol in enumerate(vol_scenarios):
        payoffs = []
        
        for S in stock_range:
            option_value = calculator.calculate_put_price(
                S, strike_price, initial_time, risk_free_rate, vol
            )
            # Use current vol premium as baseline
            current_premium = calculator.calculate_put_price(
                current_stock_price, strike_price, initial_time, risk_free_rate, vol
            )
            net_payoff = current_premium - option_value
            payoffs.append(net_payoff)
        
        ax3.plot(stock_range, payoffs, linewidth=2, 
                label=f'IV = {vol*100:.0f}%')
    
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax3.axvline(x=strike_price, color='red', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Stock Price')
    ax3.set_ylabel('Profit/Loss')
    ax3.set_title('Volatility Effect (Vega)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. 3D Surface: Time vs Volatility Effect at ATM
    time_range = np.linspace(1, 30, 20) / 365  # 1 to 30 days
    vol_range = np.linspace(0.1, 0.5, 20)     # 10% to 50% IV
    
    Time, Vol = np.meshgrid(time_range, vol_range)
    PnL = np.zeros_like(Time)
    
    for i in range(len(vol_range)):
        for j in range(len(time_range)):
            option_value = calculator.calculate_put_price(
                current_stock_price, strike_price, Time[i,j], risk_free_rate, Vol[i,j]
            )
            PnL[i,j] = option_value - initial_premium  # Negative of our P&L
    
    contour = ax4.contourf(Time*365, Vol*100, -PnL, levels=20, cmap='RdYlGn')
    ax4.contour(Time*365, Vol*100, -PnL, levels=20, colors='black', alpha=0.4, linewidths=0.5)
    fig.colorbar(contour, ax=ax4, label='Profit/Loss')
    ax4.set_xlabel('Days to Expiration')
    ax4.set_ylabel('Implied Volatility (%)')
    ax4.set_title('P&L Surface (ATM, Stock=$100)')
    
    plt.tight_layout()
    
    # Save plot to file  
    import os
    output_dir = os.environ.get('PLOT_OUTPUT_DIR', '.')
    os.makedirs(output_dir, exist_ok=True)
    filename = "SP7_short_put_analysis.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"📊 Plot saved to: {filepath}")
    
    # Also try to show if in interactive environment
    try:
        plt.show()
    except:
        print("💡 Plot saved to file (interactive display not available)")
    
    # Strategy Analysis Summary
    print(f"\n=== Strategy Analysis ===")
    print(f"Strategy: SP7 - ATM Short Put, Near Term")
    print(f"Market Bias: Bullish to Neutral")
    print(f"Profit Drivers:")
    print(f"  • Time decay (Theta positive)")
    print(f"  • Volatility crush (Vega negative)")
    print(f"  • Stock staying above breakeven")
    print(f"Risk Factors:")
    print(f"  • Sudden downward moves")
    print(f"  • Volatility expansion")
    print(f"  • Assignment if ITM at expiration")
    
    # Calculate Greeks at current conditions
    S = current_stock_price
    
    base_price = calculator.calculate_put_price(S, strike_price, initial_time, risk_free_rate, initial_volatility)
    
    # Delta (price sensitivity) - use $1 move
    price_up = calculator.calculate_put_price(S+1, strike_price, initial_time, risk_free_rate, initial_volatility)
    delta = -(price_up - base_price)  # Negative for short position
    
    # Theta (time decay) - use 1 day move
    one_day_less = max(initial_time - 1/365, 0.001/365)
    price_less_time = calculator.calculate_put_price(S, strike_price, one_day_less, risk_free_rate, initial_volatility)
    theta = -(base_price - price_less_time)  # Positive for short position (we benefit from time decay)
    
    # Vega (volatility sensitivity) - use 1% vol move
    price_high_vol = calculator.calculate_put_price(S, strike_price, initial_time, risk_free_rate, initial_volatility+0.01)
    vega = -(price_high_vol - base_price)  # Negative for short position (we lose from vol increase)
    
    print(f"\n=== Greeks Analysis ===")
    print(f"Delta: {delta:.3f} (profit ${delta:.2f} per $1 stock increase)")
    print(f"Theta: {theta:.3f} (profit ${theta:.2f} per day from time decay)")
    print(f"Vega: {vega:.3f} (loss ${-vega:.2f} per 1% vol increase)")

if __name__ == "__main__":
    short_put_payoff_analysis() 