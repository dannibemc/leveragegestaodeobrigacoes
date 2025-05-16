import streamlit as st
import pandas as pd
import datetime

# ---- 1) Autenticação simples ----
# Carrega usuário/senha de st.secrets (deixe em TOML, veja abaixo)
VALID_USER = st.secrets["login"]["username"]
VALID_PWD  = st.secrets["login"]["password"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Se não autenticado, mostra formulário de login
if not st.session_state.authenticated:
    st.title("🔒 Login")
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if u == VALID_USER and p == VALID_PWD:
            st.session_state.authenticated = True
            st.success("Autenticado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()

# ---- 2) Após autenticar, aparece a aplicação ----
st.sidebar.title("Leverage | Plataforma Inteligente")
page = st.sidebar.radio("Menu", ["Provisionamento", "IA para Obrigações", "Alertas", "Relatórios", "Crédito"])

if page == "Provisionamento":
    st.header("Dashboard de Provisões")
    st.write("Faça upload de uma planilha com suas obrigações:")
    arquivo = st.file_uploader("Selecione um .xlsx", type="xlsx")
    if arquivo:
        df = pd.read_excel(arquivo)
        st.subheader("Dados Carregados")
        st.dataframe(df)

        # Cálculos simples
        total_obr = len(df)
        provisionado = df["Valor"].sum() if "Valor" in df.columns else 0
        st.write(f"**Nº de obrigações:** {total_obr}")
        st.write(f"**Total provisionado:** R$ {provisionado:,.2f}")

        if st.button("Gerar Ação Sugerida"):
            st.info("🔍 Ação sugerida (mock): Revisar contratos com prazo próximo ou em atraso.")
    else:
        st.info("📥 Carregue a planilha para ver o dashboard.")

elif page == "IA para Obrigações":
    st.header("IA para Extração de Obrigações")
    st.write("Funcionalidade em desenvolvimento…")

elif page == "Alertas":
    st.header("Alertas de Vencimento")
    st.write("Funcionalidade em desenvolvimento…")

elif page == "Relatórios":
    st.header("Geração de Relatórios")
    st.write("Funcionalidade em desenvolvimento…")

elif page == "Crédito":
    st.header("Upload e Análise de Crédito (Serasa)")
    st.write("Funcionalidade em desenvolvimento…")
