import streamlit as st
import pandas as pd
import datetime
import requests  # Para simular a API de IA

# --- Autenticação (simplificada) ---
def autenticar():
    usuario = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")
    if usuario == "admin" and senha == "senha123":
        st.session_state["autenticado"] = True
        st.sidebar.success("Autenticado!")
    else:
        st.session_state["autenticado"] = False
        if senha:
            st.sidebar.error("Usuário ou senha incorretos")

# --- Funções de apoio ---
def simular_analise_risco(data_vencimento):
    """Simula uma chamada à API de IA para análise de risco."""
    hoje = datetime.date.today()
    dias_ate_vencimento = (data_vencimento - hoje).days
    # Simulação simples: quanto mais próximo do vencimento, maior o risco
    risco = min(100, max(0, 100 - dias_ate_vencimento * 2))
    return risco

# --- Interface do usuário ---
st.title("Leverage - Plataforma Simplificada")

if "autenticado" not in st.session_state:
    autenticar()

if st.session_state.get("autenticado"):
    st.sidebar.success("Autenticado")
    # --- Upload de dados ---
    st.header("Upload de Obrigações")
    uploaded_file = st.file_uploader("Selecione o arquivo Excel", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.subheader("Dados Carregados")
            st.dataframe(df)

            # --- Processamento dos dados ---
            df["Data de Vencimento"] = pd.to_datetime(df["Data de Vencimento"], errors='coerce')
            df = df.dropna(subset=["Data de Vencimento"])  # Remove linhas com datas inválidas

            # --- Dashboard ---
            st.header("Dashboard")
            num_obrigacoes = len(df)
            valor_total = df["Valor"].sum() if "Valor" in df.columns else 0
            col1, col2, col3 = st.columns(3)
            col1.metric("Número de Obrigações", num_obrigacoes)
            col2.metric("Valor Total", f"R$ {valor_total:,.2f}")
            # --- Alertas e análise de risco ---
            st.header("Alertas e Análise de Risco")
            for index, row in df.iterrows():
                data_vencimento = row["Data de Vencimento"].date()
                hoje = datetime.date.today()
                if data_vencimento < hoje:
                    st.warning(f"⚠️ Obrigação Vencida: {row['Descrição']} - Vencimento em {data_vencimento}")
                elif (data_vencimento - hoje).days <= 7:
                    st.warning(f"⚠️ Vencimento Próximo: {row['Descrição']} - Vencimento em {data_vencimento}")

                # --- Chamada para a API de IA (simulada) ---
                risco = simular_analise_risco(data_vencimento)
                st.write(f"Análise de Risco para {row['Descrição']}: {risco:.2f}%")

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")

else:
    st.sidebar.warning("Por favor, faça login.")
    st.stop()
