
# Real-Time Cryptocurrency Price Forecast Dashboard

This project is a real-time cryptocurrency price forecasting dashboard using Streamlit. The application fetches historical data for selected cryptocurrencies, forecasts future prices using ARIMA and SARIMA models, and displays the results in an interactive dashboard.

## Features
- Select from various cryptocurrencies (e.g., BTC, ETH, DOGE, ADA, BNB, SOL).
- View historical prices in an interactive line chart.
- View forecasted prices for the next `n` days.
- Visualize price distribution with histograms.
- See forecasted data in a table format for easy comparison.
- Automatic updates based on user input.

## Requirements
To run this application, you need the following libraries:
- Streamlit
- yfinance
- matplotlib
- statsmodels
- pandas

## Installation
1. Clone this repository or download the script file.
2. Install the required libraries:

```bash
pip install streamlit yfinance matplotlib statsmodels pandas
```

3. Run the app using the following command:

```bash
streamlit run app.py
```

4. The application will open in your default web browser, and you can start interacting with the dashboard.

## How It Works
- **Historical Data**: The app fetches cryptocurrency data using the `yfinance` library for the past 60 days.
- **ARIMA and SARIMA Models**: The app trains the ARIMA and SARIMA models to forecast the next `n` days of cryptocurrency prices.
- **Interactive Dashboard**: The user selects a cryptocurrency ticker, forecasts the number of days, and views:
  - Historical closing prices in a line chart.
  - Forecasted prices in a table and bar chart.
  - A histogram of the closing prices.
  - A combined plot of historical and forecasted prices.

## Contributions
Feel free to contribute to this project. If you have suggestions for new features or improvements, create a pull request.

## License
This project is open source and available under the MIT License.
