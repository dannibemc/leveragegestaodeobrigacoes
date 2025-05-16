import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

# 1) Carrega as credenciais dos Secrets (TOML) do Streamlit Cloud
secrets = st.secrets

# 2) Inicializa o Authenticator
auth = stauth.Authenticate(
    secrets["credentials"],
    secrets["cookie"]["name"],
    secrets["cookie"]["key"],
    secrets["cookie"]["expiry_days"],
)

# 3) Executa o login (location: 'main', 'sidebar' ou 'unrendered')
name, status, user = auth.login("Login", "main")

if status:
    auth.logout("Logout", "main")
    st.write(f"Olá, **{name}**")
    st.title("Leverage – Gestão de Obrigações")

    # 4) Upload de Excel
    st.header("Upload de planilha de obrigações")
    excel = st.file_uploader("Selecione um arquivo .xlsx", type=["xlsx"])
    if excel:
        df = pd.read_excel(excel)
        st.subheader("Dados brutos")
        st.dataframe(df)

        # 5) Estruturação das obrigações
        obr = []
        for _, r in df.iterrows():
            obr.append({
                "ParteDevedora": "Devedora",
                "Documento":     r.get("Documento",     "Não especificado"),
                "Cláusula":      r.get("Cláusula",      "Não especificado"),
                "Resumo":        r.get("Resumo",        "Não especificado"),
                "DataOrigem":    r.get("DataOrigem",    "Não especificado"),
                "Periodicidade": r.get("Periodicidade", "Não especificado"),
            })
        st.subheader("Obrigações Estruturadas")
        st.json(obr)

    # 6) Dashboard simples
    st.header("Dashboard")
    total = len(df) if "df" in locals() else 0
    c1, c2 = st.columns(2)
    c1.metric("Total de Obrigações", total)
    c2.metric("Total Provisionado (R$)", "R$ 180 000,00")

elif status is False:
    st.error("Usuário ou senha inválidos")
else:
    st.warning("Digite usuário e senha")
