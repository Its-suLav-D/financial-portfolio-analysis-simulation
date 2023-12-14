import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Financial Portfolio Analysis Simulator", layout="wide")


st.title("Financial Portfolio Analysis Simulator")


# Sidebar - User Input Parameters
st.sidebar.header('User Input Parameters')

start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2010-01-06'))
end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-12-30'))

# Additional Parameters
tax_rate = st.sidebar.number_input('Tax Rate', 0.15)
inflation_rate = st.sidebar.number_input('Inflation Rate', 0.02)
initial_investment = st.sidebar.number_input('Initial Investment', 10000)
# Sidebar - Market Condition Selection
st.sidebar.subheader('Market Condition Simulation')
selected_market_condition = st.sidebar.selectbox(
    "Select a Market Condition to Simulate", 
    ['None', 'Bull', 'Bear', 'Volatile']
)

# Conditionally show start and end date input based on the selected market condition
if selected_market_condition != 'None':
    condition_start_date = st.sidebar.date_input(f'{selected_market_condition} Market Start Date', pd.to_datetime('2021-01-01'))
    condition_end_date = st.sidebar.date_input(f'{selected_market_condition} Market End Date', pd.to_datetime('2021-06-30'))

    condition_start_date = pd.Timestamp(condition_start_date)
    condition_end_date = pd.Timestamp(condition_end_date)

else:
    condition_start_date, condition_end_date = None, None


st.sidebar.subheader("Scenarios ")
selected_scenario = st.sidebar.selectbox(
    "Select a Scenario",
    ['None', 'Market Crash', 'Economic Boom', 'Downturn', 'Growth']
)

if selected_scenario != 'None':
    scenario_date_start = st.sidebar.date_input(f'{selected_scenario} Date', pd.to_datetime('2021-01-01'))
    scenario_date_end = st.sidebar.date_input(f'{selected_scenario} Date', pd.to_datetime('2021-06-30'))
    scenario_value = st.sidebar.number_input(f'{selected_scenario} Value', 0.8)

    scenario_date_start = pd.Timestamp(scenario_date_start)
    scenario_date_end = pd.Timestamp(scenario_date_end)
else:
    scenario_date_start, scenario_date_end, scenario_value = None, None, None


market_conditions_options = {
    '2018-01-02: Bull': ('2019-01-02', 'bull'),
    '2015-10-16: Bear': ('2015-10-16', 'bear'),
    '2011-07-11: Volatile': ('2011-07-11', 'volatile')
}

scenarios_options = {
    '2020-07-16: Market Crash (0.8)': ('2020-07-16', 0.8),
    '2018-10-16: Economic Boom (1.2)': ('2018-10-16', 1.2),
    '2022-01-02: Downturn (0.9)': ('2012-01-02', 0.9),
    '2023-07-01: Growth (1.1)': ('2023-07-01', 1.1)
}

# Allocation for different strategies
allocations = {
    'Conservative': {'AAPL': 0.10, 'MSFT': 0.10, 'AGG': 0.70, 'SPY': 0.05, 'QQQ': 0.05},
    'Balanced': {'AAPL': 0.15, 'MSFT': 0.15, 'AGG': 0.40, 'SPY': 0.15, 'QQQ': 0.15},
    'Aggressive': {'AAPL': 0.20, 'MSFT': 0.20, 'AGG': 0.20, 'SPY': 0.20, 'QQQ': 0.20}
}


# Sidebar - Portfolio Allocation Selection
st.sidebar.subheader('Portfolio Allocation Strategy')
selected_allocation_strategy = st.sidebar.radio(
    "Choose an allocation strategy",
    list(allocations.keys())
)

# Fixed assets and transition matrix
assets = ['AAPL', 'MSFT', 'AGG', 'SPY', 'QQQ']

states = ["Bull", "Bear", "Stable"]
transition_matrix = np.array([
    [0.6, 0.2, 0.2],
    [0.3, 0.4, 0.3],
    [0.2, 0.2, 0.6]
])

# Allocation for different strategies
conservative_alloc = {'AAPL': 0.10, 'MSFT': 0.10, 'AGG': 0.70, 'SPY': 0.05, 'QQQ': 0.05}
balanced_alloc = {'AAPL': 0.15, 'MSFT': 0.15, 'AGG': 0.40, 'SPY': 0.15, 'QQQ': 0.15}
aggressive_alloc = {'AAPL': 0.20, 'MSFT': 0.20, 'AGG': 0.20, 'SPY': 0.20, 'QQQ': 0.20}

def calculate_portfolio_returns(alloc, daily_returns):
    portfolio_weights = [alloc[asset] for asset in daily_returns.columns]
    portfolio_returns = daily_returns.dot(portfolio_weights)
    print("Portfolio returns:", portfolio_returns.iloc[0])
    return portfolio_returns


def apply_market_condition(returns, condition):
    if condition == 'Bull':
        return returns * 1.55  
    elif condition == 'Bear':
        return returns * 0.95  
    elif condition == 'Volatile':
        return returns * np.random.normal(1.0, 0.05) 
    else:
        return returns


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


def simulate_market_states(start_date, end_date, initial_state, transition_matrix):
    states = ["Bull", "Bear", "Stable"]
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    market_states = [initial_state]

    for _ in range(1, len(dates)):
        current_state_index = states.index(market_states[-1])
        next_state = np.random.choice(states, p=transition_matrix[current_state_index])
        market_states.append(next_state)

    return pd.Series(market_states, index=dates)



def calculate_performance_metrics(portfolio_returns, risk_free_rate=0.01):
    # Convert daily returns to annual returns
    annual_returns = (1 + portfolio_returns).resample('Y').prod() - 1

    # Calculate average annual return
    avg_annual_return = annual_returns.mean()

    # Calculate annualized standard deviation (risk)
    annual_std_dev = annual_returns.std()

    # Calculate the Sharpe Ratio
    sharpe_ratio = (avg_annual_return - risk_free_rate) / annual_std_dev

    return avg_annual_return, annual_std_dev, sharpe_ratio


# Downloading Data
@st.cache_data
def download_data():
    return yf.download(assets, start=start_date, end=end_date)

data = download_data()


daily_returns = data['Adj Close'].pct_change()


st.write("## Selected Parameters and Settings")

col1, col2 = st.columns(2)

with col1:
    st.write("### User Input Parameters")
    st.write("Start Date:", start_date)
    st.write("End Date:", end_date)
    st.write("Tax Rate:", tax_rate)
    st.write("Inflation Rate:", inflation_rate)
    st.write("Initial Investment:", initial_investment)

with col2:
    st.write("### Market Condition")
    st.write("Selected Market Condition:", selected_market_condition, "-", condition_start_date, "to", condition_end_date)
    st.write("### Scenario")
    st.write("Selected Scenario:", selected_scenario, "-", scenario_date_start, "to", scenario_date_end, ":", scenario_value)
    st.write("### Allocation Strategy")
    st.write("Selected Allocation Strategy:", selected_allocation_strategy, " - ", allocations[selected_allocation_strategy])
st.write("#### Daily Returns")
st.write(daily_returns)



portfolio_allocations = allocations[selected_allocation_strategy]
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = {}


if st.sidebar.button('Run Simulation'):
    simulated_portfolio = simulate_portfolio_with_scenarios(
        portfolio_allocations=portfolio_allocations,
        start_date=start_date, 
        end_date=end_date, 
        initial_investment=initial_investment, 
        tax_rate=tax_rate, 
        inflation_rate=inflation_rate, 
        selected_market_condition=selected_market_condition,  
        condition_start_date=condition_start_date, 
        condition_end_date=condition_end_date,  
        scenario_start_date=scenario_date_start,  
        scenario_end_date=scenario_date_end,      
        scenario_impact=scenario_value            
    )

    # Displaying the results of the simulation
    st.write("#### Simulated Portfolio Performance")
    # Generate a unique key for this simulation (e.g., using the current timestamp)
    sim_key = datetime.now().strftime("%Y%m%d%H%M%S")

    st.session_state.simulation_data[sim_key] = simulated_portfolio
    st.line_chart(simulated_portfolio)



# Dropdown for selecting a simulation run
if len(st.session_state.simulation_data) > 0:
    sim_keys = list(st.session_state.simulation_data.keys())
    default_selection = "Select a simulation run"
    selected_sim = st.selectbox("Select a simulation run to view", [default_selection] + sim_keys)

    if selected_sim != default_selection and selected_sim in st.session_state.simulation_data:
        st.line_chart(st.session_state.simulation_data[selected_sim])
