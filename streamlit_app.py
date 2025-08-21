
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(page_title="Fin Agent Dashboard", layout="wide")
st.title("📈 Fin Agent - Primeira Versão")

ticker = st.selectbox("Escolha um ativo", ["EURUSD=X", "GBPUSD=X", "BTC-USD", "ETH-USD", "AAPL", "TSLA", "PETR4.SA", "VALE3.SA", "GOLD=X"])

data = yf.download(ticker, period="5d", interval="15m")

fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name="Candlesticks"
))
fig.update_layout(xaxis_rangeslider_visible=False, height=600)

st.plotly_chart(fig, use_container_width=True)
