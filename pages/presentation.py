import streamlit as st

assets = ['AAPL', 'MSFT', 'AGG', 'SPY', 'QQQ']

st.write(""" Assets """)
st.write("""
- **AAPL**: Apple Inc.
- **MSFT**: Microsoft Corporation
- **AGG**: iShares Core U.S. Aggregate Bond ETF
- **SPY**: SPDR S&P 500 ETF Trust
- **QQQ**: Invesco QQQ Trust (tracks the NASDAQ-100 Index)    
""")


st.write("""
         
It Covers key financial concepts like market conditions (Bull, Bear, Volatile), investment scenarios (Market Crash, Economic Boom, etc.), and portfolio strategies (Conservative, Balanced, Aggressive).
It demonstrates how different market conditions and scenarios can impact investment returns.
                 
""")


st.code("""
def simulate_portfolio_with_scenarios(portfolio_allocations, start_date, end_date, initial_investment, tax_rate, inflation_rate, selected_market_condition, condition_start_date, condition_end_date, scenario_start_date, scenario_end_date, scenario_impact):
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    simulated_values = [initial_investment]
    previous_value = initial_investment
    capital_gains = 0

    for date in dates[1:]:
        if date in daily_returns.index:
            daily_return_data = daily_returns.loc[[date]]
            if not daily_return_data.empty:
                daily_return = calculate_portfolio_returns(portfolio_allocations, daily_return_data)

                # Apply market condition if within range
                if selected_market_condition != 'None' and condition_start_date is not None and condition_end_date is not None and condition_start_date <= date <= condition_end_date:
                    daily_return = apply_market_condition(daily_return.iloc[0], selected_market_condition)
                else:
                    daily_return = daily_return.iloc[0]

                # Apply scenario impact if within range
                if scenario_start_date is not None and scenario_end_date is not None and scenario_start_date <= date <= scenario_end_date:
                    daily_return *= scenario_impact

                # Apply the daily return to update portfolio value
                new_value = previous_value * (1 + daily_return)

                # Accumulate capital gains for tax calculation
                capital_gains += max(0, new_value - previous_value)

                simulated_values.append(new_value)
                previous_value = new_value
        else:
            simulated_values.append(previous_value)

    # Adjust final portfolio value for inflation and tax
    final_value = simulated_values[-1] * (1 - inflation_rate)
    tax_amount = capital_gains * tax_rate
    final_value -= tax_amount
    simulated_values[-1] = final_value

    return pd.Series(simulated_values, index=dates)


""", language='python')

st.subheader("Futuere Work")

st.write("""

As part of my future plan in finance, I intend to utilize the transition_matrix, a crucial component in Markov chain modeling, to predict and analyze market states like 'Bull', 'Bear', and 'Stable'. This matrix is fascinating because each element signifies the probability of moving from one market condition to another. For instance, it can tell us the likelihood of a 'Bull' market staying bullish or turning bearish in the next time period. My goal is to leverage this tool for better forecasting market trends, which is essential for strategic investment planning. By simulating various market scenarios, I aim to enhance my approach to risk management and investment strategy, making well-informed decisions in a field where market dynamics are constantly evolving.
         
""")