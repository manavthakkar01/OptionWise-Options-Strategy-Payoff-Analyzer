# OptionWise – Options Strategy Payoff Analyzer

A beginner-friendly Python + Streamlit project for understanding basic options strategies.

## Features
- Long Call, Long Put, Short Call, Short Put
- Bull Call Spread and Long Straddle
- Expiry profit/loss calculations
- Breakeven calculations
- Payoff graph
- Downloadable CSV payoff table

## Technology
- Python
- NumPy
- Pandas
- Matplotlib
- Streamlit

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Start the application:

   `streamlit run app.py`

## Important assumptions
- The project calculates simplified payoff at expiry, not the changing market value of an option before expiry.
- It excludes brokerage, taxes, slippage, lot-size multiplication, and margin requirements.
- Values are hypothetical and for learning only. It is not investment advice.

## Suggested interview explanation
"I built OptionWise to understand how basic options strategies behave at expiry. The user enters the underlying price, strike price, and option premium. Python and NumPy calculate profit or loss across a range of possible expiry prices. Matplotlib displays the payoff graph, and Streamlit makes the tool interactive. I also added breakeven calculations and strategy comparison."
