import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

# Carrega credenciais e configurações do Streamlit Cloud Secrets
secrets = st.secrets

auth = stauth.Authenticate(
    secrets["credentials"],
    secrets["cookie"]["name"],
    secrets["cookie"]["key"],
    secrets["cookie"]["expiry_days"]
)

# chama o login; location deve ser 'main' | 'sidebar' | 'unrendered'
name, status, username = auth.login("Login", "main")

if status:
    auth.logout("Logout", "main")
    st.write(f"Olá, **{name}**")
    st.title("Leverage - Gestão de Obrigações")

    # Upload de Excel
    excel = st.file_uploader("Selecione .xlsx", type=["xlsx"])
    if excel:
        df = pd.read_excel(excel)
        st.subheader("Dados brutos")
        st.dataframe(df)

        obr = []
        for _, r in df.iterrows():
            obr.append({
                "ParteDevedora": "Devedora",
                "Documento": r.get("Documento", "Não especificado"),
                "Cláusula":  r.get("Cláusula",  "Não especificado"),
                "Resumo":    r.get("Resumo",    "Não especificado"),
                "DataOrigem":r.get("DataOrigem","Não especificado"),
                "Periodicidade": r.get("Periodicidade","Não especificado"),
            })
        st.subheader("Obrigações Estruturadas")
        st.json(obr)

    # Dashboard mock
    st.header("Dashboard")
    col1, col2 = st.columns(2)
    total = len(df) if "df" in locals() else 0
    col1.metric("Total de Obrigações", total)
    col2.metric("Provisionado (R$)", "R$ 180.000,00")

elif status is False:
    st.error("Usuário ou senha inválidos")
else:
    st.warning("Digite usuário e senha")

