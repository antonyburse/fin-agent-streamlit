
# Fin Agent Streamlit - Primeira Versão

Este é o dashboard inicial do agente de análise financeira.

## Como publicar no Render

1. Crie um repositório GitHub e suba todos os arquivos.
2. No Render, clique em **New Web Service** e conecte sua conta GitHub.
3. Escolha o repositório `fin-agent-streamlit`.
4. No **Start Command**, coloque:
   ```
   streamlit run streamlit_app.py --server.port=10000 --server.address=0.0.0.0
   ```
5. Render vai instalar dependências e gerar um link público.
