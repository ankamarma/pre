import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to fetch stock data
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo", interval="1h")
    return data

# Function to calculate indicators and predict price
def predict_price(symbol):
    data = get_stock_data(symbol)
    if data.empty:
        return None, None

    # Use pandas-ta instead of TA-Lib
    data["50_MA"] = data["Close"].rolling(window=50).mean()
    data["ATR"] = ta.atr(high=data["High"], low=data["Low"], close=data["Close"], length=14)

    last_price = data["Close"].iloc[-1]
    returns = data["Close"].pct_change().dropna()

    # Monte Carlo simulation for next price range
    mean = np.mean(returns)
    std_dev = np.std(returns)
    
    simulations = 1000
    days = 3
    price_paths = []

    for _ in range(simulations):
        future_prices = [last_price]
        for _ in range(days):
            next_price = future_prices[-1] * (1 + np.random.normal(mean, std_dev))
            future_prices.append(next_price)
        price_paths.append(future_prices)

    predicted_prices = np.array(price_paths)
    lower_bound = np.percentile(predicted_prices[:, -1], 10)
    upper_bound = np.percentile(predicted_prices[:, -1], 90)

    return round(lower_bound, 2), round(upper_bound, 2)

@app.route("/predict", methods=["GET"])
def forecast():
    symbol = request.args.get("symbol", "").upper()
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    low, high = predict_price(symbol)
    if low is None:
        return jsonify({"error": "Invalid stock symbol or no data available"}), 404

    return jsonify({"symbol": symbol, "low": low, "high": high})

if __name__ == "__main__":
    app.run(debug=True)
