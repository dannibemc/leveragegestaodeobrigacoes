import streamlit as st
import pandas as pd
import datetime

# Autenticação simples (fixa)
USUARIO = "admin"
SENHA = "senha123"

# Login
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 Por favor, faça login")
    usuario_input = st.text_input("Usuário")
    senha_input = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario_input == USUARIO and senha_input == SENHA:
            st.session_state.autenticado = True
            st.success("Autenticado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()

# Após login, mostra a plataforma
st.sidebar.title("Leverage | Plataforma Simplificada")
menu = st.sidebar.radio("Menu", ["Provisões", "IA", "Alertas", "Relatórios", "Crédito"])

if menu == "Provisões":
    st.header("Dashboard de Provisões")
    uploaded_file = st.file_uploader("Faça upload da planilha de obrigações", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.subheader("Dados carregados")
        st.dataframe(df)

        total_obrigacoes = len(df)
        total_valor = df["Valor"].sum() if "Valor" in df.columns else 0
        st.write(f"Número de obrigações: {total_obrigacoes}")
        st.write(f"Valor total provisionado: R$ {total_valor:,.2f}")

        if st.button("Gerar Ação Sugerida"):
            st.info("Revisar contratos com vencimento próximo ou atrasado.")

elif menu == "IA":
    st.header("IA para Obrigações")
    st.write("Funcionalidade em desenvolvimento...")

elif menu == "Alertas":
    st.header("Alertas de Vencimento")
    st.write("Funcionalidade em desenvolvimento...")

elif menu == "Relatórios":
    st.header("Geração de Relatórios")
    st.write("Funcionalidade em desenvolvimento...")

elif menu == "Crédito":
    st.header("Análise de Crédito")
    st.write("Funcionalidade em desenvolvimento...")

