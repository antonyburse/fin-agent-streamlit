import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

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

    # Calcula EMAs e ATR
    data["EMA50"] = data["Close"].ewm(span=50, adjust=False).mean()
    data["EMA200"] = data["Close"].ewm(span=200, adjust=False).mean()
    data["ATR"] = (data["High"] - data["Low"]).rolling(14).mean()

    # Verifica se as colunas necessárias existem
    required_cols = ["Close", "EMA50", "EMA200", "ATR"]
    if not all(col in data.columns for col in required_cols):
        st.write(f"Sem dados válidos para {ticker}")
        continue

    # Remove NaNs
    data = data.dropna(subset=required_cols)
    if data.empty:
        st.write(f"Sem dados válidos para {ticker}")
        continue

    last = data.iloc[-1]

    ema50 = last["EMA50"]
    ema200 = last["EMA200"]
    close = last["Close"]
    atr = last["ATR"]

    signal = "⛔ Neutro"
    if ema50 > ema200:
        signal = "🟢 Compra"
    elif ema50 < ema200:
        signal = "🔴 Venda"

    sl = close - 1.5*atr if signal=="🟢 Compra" else close + 1.5*atr
    tp = close + 3*atr if signal=="🟢 Compra" else close - 3*atr

    st.subheader(f"{ticker}")
    st.write(f"Sinal: {signal}")
    st.write(f"Entrada: {close:.2f}, SL: {sl:.2f}, TP: {tp:.2f}")
