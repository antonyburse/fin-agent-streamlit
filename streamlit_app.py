import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="Fin Agent Dashboard", layout="wide")

st.set_page_config(page_title="Fin Agent Dashboard", layout="wide")
st.title("📈 Fin Agent - Sinais Diários")

# Lista de ativos
tickers = ["EURUSD=X", "USDJPY=X", "GBPUSD=X", "XAUUSD=X", 
           "BTC-USD", "ETH-USD", "PETR4.SA", "VALE3.SA", 
           "ITUB4.SA", "AAPL", "MSFT", "AMZN"]

# Seleção de data
start_date = st.date_input("Data inicial", datetime.date.today() - datetime.timedelta(days=365))
end_date = st.date_input("Data final", datetime.date.today())

for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        st.write(f"Sem dados para {ticker}")
        continue
    data["EMA50"] = data["Close"].ewm(span=50, adjust=False).mean()
    data["EMA200"] = data["Close"].ewm(span=200, adjust=False).mean()
    data["ATR"] = (data["High"] - data["Low"]).rolling(14).mean()
    
    last = data.iloc[-1]
    signal = "⛔ Neutro"
    if last["EMA50"] > last["EMA200"]:
        signal = "🟢 Compra"
    elif last["EMA50"] < last["EMA200"]:
        signal = "🔴 Venda"
    
    sl = last["Close"] - 1.5*last["ATR"] if signal=="🟢 Compra" else last["Close"] + 1.5*last["ATR"]
    tp = last["Close"] + 3*last["ATR"] if signal=="🟢 Compra" else last["Close"] - 3*last["ATR"]
    
    st.subheader(f"{ticker}")
    st.write(f"Sinal: {signal}")
    st.write(f"Entrada: {last['Close']:.2f}, SL: {sl:.2f}, TP: {tp:.2f}")
