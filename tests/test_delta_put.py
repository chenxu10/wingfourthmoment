from delta_calculator import OptionCalculator

def main():
    calculator = OptionCalculator()
    underlying_price = 82.13  # Match Fidelity data
    strike_price = 84
    time_to_expiry = 0.001  # expires today
    risk_free_rate = 0.04  # 4%
    volatility = 0.93  # 84.41% from Fidelity IV
    print(volatility)
    delta = calculator.calculate_put_delta(
        underlying_price, strike_price, time_to_expiry, risk_free_rate, volatility
    )
    print(delta)

if __name__ == "__main__":
    main()