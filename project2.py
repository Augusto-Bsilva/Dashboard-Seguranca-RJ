import streamlit as st 
import yfinance as yf
import pandas as pd 
import datetime as date

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("Realtime Stock Dashboard")

st.sidebar.header("Stock Settings")
ticker_symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
period = st.sidebar.selectbox("Select Period",["1d","5d","1mo","6mo","1y","5y"])
intervaal = st.sidebar.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d"])

ticker = yf.Ticker(ticker_symbol)
data = ticker.history(period=period, interval=intervaal)

latest_price = data["Close"].iloc[-1] if not data.empty else "N/A"
st.metric(label=f"Current Price: {ticker_symbol}", value=f"${latest_price:.2f}" if latest_price != "N/A" else "No Data Available")

st.subheader(f"Price Chart for {ticker_symbol}")
if not data.empty:
    st.line_chart(data['Close'])
else:
    st.warning("No data available for this symbol")

col1, col2, col3 =  st.columns(3)
with col1:
    st.write("**Previous Close:**", ticker.info.get("previousClose", "N/A"))
with col2:
    st.write("**Market Cap:**", ticker.info.get("marketCap", "N/A"))
with col3:
    st.write("**52 Week High:**", ticker.info.get("fiftyTwoWeekHigh", "N/A"))

st.caption("Refreseh page for updated data or adjust interval")