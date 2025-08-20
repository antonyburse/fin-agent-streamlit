# Fin Agent Streamlit

Dashboard Streamlit com sinais diários de ativos (Forex, Gold, Cripto, Ações BR/US) usando EMA50/EMA200 e ATR para SL/TP.

## Deploy no Render
1. Vá em https://render.com e faça login.
2. Clique em **New → Web Service → Connect GitHub**.
3. Escolha este repositório.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run streamlit_app.py --server.port $PORT`
6. Deploy → URL pública para acessar no celular.
