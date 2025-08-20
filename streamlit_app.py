import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="Fin Agent Dashboard", layout="wide")
st.title("📊 Fin Agent - Análises Diárias")

# Lista de ativos (Forex, Ouro, Criptos, Ações Brasil e EUA)
assets = {
    "EURUSD=X": "Euro/USD",
    "GBPUSD=X": "Libra/USD",
    "USDJPY=X": "USD/JPY",
    "XAUUSD=X": "Ouro",
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "PETR4.SA": "Petrobras",
    "VALE3.SA": "Vale",
    "ITUB4.SA": "Itaú",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon"
}

# Período de análise
end = datetime.datetime.now()
start = end - datetime.timedelta(days=200)

# Função para indicadores técnicos
def add_indicators(df):
    df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["EMA200"] = df["Close"].ewm(span=200, adjust=False).mean()
    df["ATR"] = (df["High"] - df["Low"]).rolling(window=14).mean()
    return df

# Loop pelos ativos
for ticker, name in assets.items():
    st.subheader(f"🔹 {name} ({ticker})")
    
    try:
        data = yf.download(ticker, start=start, end=end, interval="1d")
        if data.empty:
            st.write("Sem dados disponíveis.")
            continue

        data = add_indicators(data)

        # Verifica se as colunas existem
        required_cols = ["Close", "EMA50", "EMA200", "ATR"]
        if not all(col in data.columns for col in required_cols):
            st.write("Sem dados válidos para este ativo.")
            continue

        data = data.dropna(subset=required_cols)
        if data.empty:
            st.write("Sem dados válidos após limpeza.")
            continue

        last = data.iloc[-1]

        # Estratégia simples: cruzamento de médias
        if last["EMA50"] > last["EMA200"]:
            signal = "🟢 Compra"
            stop = round(last["Close"] - 2 * last["ATR"], 2)
            target = round(last["Close"] + 2 * last["ATR"], 2)
        else:
            signal = "🔴 Venda"
            stop = round(last["Close"] + 2 * last["ATR"], 2)
            target = round(last["Close"] - 2 * last["ATR"], 2)

        # Exibir informações
        st.write(f"**Sinal:** {signal}")
        st.write(f"📌 Preço atual: {round(last['Close'], 2)}")
        st.write(f"⛔ Stop Loss: {stop}")
        st.write(f"🎯 Take Profit: {target}")

        # Gráfico
        st.line_chart(data[["Close", "EMA50", "EMA200"]])

    except Exception as e:
        st.error(f"Erro ao processar {ticker}: {e}")
