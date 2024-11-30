import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta

# Fetch latest cryptocurrency data
def fetch_latest_crypto_data(ticker, days=60):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days)
    data = yf.download(ticker + "-USD", start=start_date, end=end_date, interval="1d")
    return data.dropna()

# Train and forecast using ARIMA or SARIMA
def train_and_forecast(data, forecast_days):
    best_model = None
    best_aic = float("inf")
    forecasted_prices = None

    # Try ARIMA models
    for p in range(1, 3):
        for d in range(0, 2):
            for q in range(1, 3):
                try:
                    model = ARIMA(data['Close'], order=(p, d, q))
                    fitted_model = model.fit()
                    aic = fitted_model.aic
                    if aic < best_aic:
                        best_aic = aic
                        best_model = fitted_model
                        forecasted_prices = fitted_model.forecast(steps=forecast_days)
                except:
                    continue

    # Try SARIMA models
    for p in range(1, 3):
        for d in range(0, 2):
            for q in range(1, 3):
                for P in range(0, 2):
                    for D in range(0, 2):
                        for Q in range(0, 2):
                            for s in [7, 30]:  # Weekly or monthly seasonality
                                try:
                                    model = SARIMAX(data['Close'], order=(p, d, q), seasonal_order=(P, D, Q, s))
                                    fitted_model = model.fit(disp=False)
                                    aic = fitted_model.aic
                                    if aic < best_aic:
                                        best_aic = aic
                                        best_model = fitted_model
                                        forecasted_prices = fitted_model.forecast(steps=forecast_days)
                                except:
                                    continue

    return forecasted_prices

# Plot historical and forecasted prices
def plot_forecast(data, forecast_dates, forecasted_prices, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label=f'{ticker} Historical Prices', color='blue')
    plt.plot(forecast_dates, forecasted_prices, label=f'{ticker} Forecasted Prices', color='orange')
    plt.title(f"{ticker} Cryptocurrency Price Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit app setup
st.set_page_config(page_title="Cryptocurrency Price Forecast", layout="wide")
st.title("Real-Time Cryptocurrency Price Forecast")

# Sidebar for ticker input
st.sidebar.header("Input")
tickers = st.sidebar.selectbox(
    "Select Cryptocurrency (e.g., BTC, ETH, DOGE):",
    options=["BTC", "ETH", "DOGE", "ADA", "BNB", "SOL"],
    index=0  # Default selected as "BTC"
)

forecast_days = st.sidebar.slider("Select Forecast Days", min_value=1, max_value=30, value=7)

# Main Content Layout
col1, col2 = st.columns([1, 2])  # Left column smaller for settings, right column larger for visualizations

# Ticker and forecast information on the left column
with col1:
    st.write(f"### Selected Cryptocurrency: {tickers}-USD")
    st.write(f"Forecast for the next {forecast_days} days.")

# Forecasting and visualizations on the right column
with col2:
    # Fetch data and display summary
    data = fetch_latest_crypto_data(tickers)
    st.write(f"Fetched {len(data)} days of data for {tickers}-USD")
    st.write(f"### {tickers} Historical Prices")
    st.line_chart(data['Close'])

    # Train model and display forecast
    forecast_dates = pd.date_range(data.index[-1] + timedelta(days=1), periods=forecast_days, freq='B')
    forecasted_prices = train_and_forecast(data, forecast_days)
    
    # Show forecasted data in a DataFrame
    forecast_df = pd.DataFrame({"Date": forecast_dates, "Forecasted Price (USD)": forecasted_prices})
    st.write(f"### Forecasted Prices for {tickers}-USD")
    st.dataframe(forecast_df)  # Display forecasted data in a table

    # Show histogram of historical closing prices
    st.write(f"### {tickers} Price Distribution")
    fig, ax = plt.subplots()
    ax.hist(data['Close'], bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f"{tickers} Closing Price Distribution")
    ax.set_xlabel("Price (USD)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Plot combined historical and forecasted prices
    plot_forecast(data, forecast_dates, forecasted_prices, tickers)
