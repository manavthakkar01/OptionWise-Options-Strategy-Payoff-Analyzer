import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="OptionWise", page_icon="📈", layout="wide")

st.title("📈 OptionWise – Options Strategy Payoff Analyzer")
st.caption("A beginner-friendly tool to understand option payoff, profit/loss, and breakeven.")

st.info("Educational simulator only. It uses hypothetical expiry prices and does not provide investment advice.")

strategy = st.selectbox(
    "Choose an options strategy",
    ["Long Call", "Long Put", "Short Call", "Short Put", "Bull Call Spread", "Long Straddle"]
)

col1, col2, col3 = st.columns(3)
with col1:
    spot = st.number_input("Current underlying price (₹)", min_value=0.01, value=100.0, step=1.0)
with col2:
    strike = st.number_input("Strike price (₹)", min_value=0.01, value=100.0, step=1.0)
with col3:
    premium = st.number_input("Premium (₹)", min_value=0.0, value=5.0, step=0.5)

if strategy == "Bull Call Spread":
    col4, col5 = st.columns(2)
    with col4:
        upper_strike = st.number_input("Higher strike price (₹)", min_value=float(strike), value=float(strike + 10), step=1.0)
    with col5:
        upper_premium = st.number_input("Premium received for higher-strike call (₹)", min_value=0.0, value=2.0, step=0.5)
elif strategy == "Long Straddle":
    put_premium = st.number_input("Put premium (₹)", min_value=0.0, value=5.0, step=0.5)

def payoff_long_call(prices, k, p):
    return np.maximum(prices - k, 0) - p

def payoff_long_put(prices, k, p):
    return np.maximum(k - prices, 0) - p

if st.button("Calculate payoff", type="primary"):
    low = max(0, spot * 0.5)
    high = spot * 1.5
    prices = np.linspace(low, high, 301)

    if strategy == "Long Call":
        pnl = payoff_long_call(prices, strike, premium)
        breakeven = strike + premium
        max_profit = "Unlimited"
        max_loss = f"₹{premium:.2f} per unit"
        breakeven_text = f"₹{breakeven:.2f}"
    elif strategy == "Long Put":
        pnl = payoff_long_put(prices, strike, premium)
        breakeven = strike - premium
        max_profit = f"₹{max(strike - premium, 0):.2f} per unit"
        max_loss = f"₹{premium:.2f} per unit"
        breakeven_text = f"₹{breakeven:.2f}"
    elif strategy == "Short Call":
        pnl = -payoff_long_call(prices, strike, premium)
        breakeven = strike + premium
        max_profit = f"₹{premium:.2f} per unit"
        max_loss = "Unlimited"
        breakeven_text = f"₹{breakeven:.2f}"
    elif strategy == "Short Put":
        pnl = -payoff_long_put(prices, strike, premium)
        breakeven = strike - premium
        max_profit = f"₹{premium:.2f} per unit"
        max_loss = f"₹{max(strike - premium, 0):.2f} per unit (if price falls to zero)"
        breakeven_text = f"₹{breakeven:.2f}"
    elif strategy == "Bull Call Spread":
        if upper_strike <= strike:
            st.error("Higher strike must be greater than the lower strike.")
            st.stop()
        pnl = payoff_long_call(prices, strike, premium) - np.maximum(prices - upper_strike, 0) + upper_premium
        net_debit = premium - upper_premium
        breakeven = strike + net_debit
        max_profit_value = upper_strike - strike - net_debit
        max_profit = f"₹{max(max_profit_value, 0):.2f} per unit"
        max_loss = f"₹{max(net_debit, 0):.2f} per unit"
        breakeven_text = f"₹{breakeven:.2f}"
    else:  # Long Straddle
        pnl = payoff_long_call(prices, strike, premium) + payoff_long_put(prices, strike, put_premium)
        total_premium = premium + put_premium
        lower_be = strike - total_premium
        upper_be = strike + total_premium
        max_profit = "Potentially unlimited on upside"
        max_loss = f"₹{total_premium:.2f} per unit"
        breakeven_text = f"₹{lower_be:.2f} and ₹{upper_be:.2f}"

    best_idx = int(np.argmax(pnl))
    worst_idx = int(np.argmin(pnl))
    m1, m2, m3 = st.columns(3)
    m1.metric("Maximum profit", max_profit)
    m2.metric("Maximum loss", max_loss)
    m3.metric("Breakeven price", breakeven_text)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(prices, pnl, label="Profit / Loss")
    ax.axhline(0, linewidth=1)
    ax.axvline(spot, linestyle="--", linewidth=1, label="Current price")
    ax.set_xlabel("Underlying price at expiry (₹)")
    ax.set_ylabel("Profit / Loss per unit (₹)")
    ax.set_title(f"{strategy} – Expiry Payoff")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

    results = pd.DataFrame({
        "Underlying price at expiry (₹)": np.round(prices, 2),
        "Profit / Loss per unit (₹)": np.round(pnl, 2)
    })
    st.subheader("Payoff table")
    st.dataframe(results.iloc[::15].reset_index(drop=True), use_container_width=True)
    st.download_button(
        "Download payoff data (CSV)",
        results.to_csv(index=False).encode("utf-8"),
        file_name="optionwise_payoff.csv",
        mime="text/csv"
    )

st.divider()
st.subheader("Quick concepts")
st.markdown("""
- **Call option:** Gives the buyer the right, but not the obligation, to buy the underlying at the strike price.
- **Put option:** Gives the buyer the right, but not the obligation, to sell the underlying at the strike price.
- **Premium:** The price paid by the option buyer.
- **Breakeven:** The expiry price at which profit/loss becomes zero.
- **Payoff chart:** Shows how profit or loss changes at different expiry prices.
""")
