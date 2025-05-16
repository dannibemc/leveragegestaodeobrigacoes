import streamlit as st
import streamlit_authenticator as stauth
import yaml
import pandas as pd

# 1) Carregar credenciais
with open('config.yaml') as f:
    config = yaml.safe_load(f)

auth = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


name, status, user = auth.login('Login', 'main')
if status:
    auth.logout('Logout', 'main')
    st.write(f'Olá, **{name}**')
    st.title('Leverage - Gestão de Obrigações')
    
    # 2) Upload de Excel
    st.header('Upload de obrigações')
    excel = st.file_uploader('Selecione .xlsx', type=['xlsx'])
    if excel:
        df = pd.read_excel(excel)
        st.subheader('Dados brutos')
        st.dataframe(df)
        # 3) Estruturação
        obr = []
        for _, r in df.iterrows():
            obr.append({
                'ParteDevedora': 'Devedora',
                'Documento': r.get('Documento','Não especificado'),
                'Cláusula': r.get('Cláusula','Não especificado'),
                'Resumo': r.get('Resumo','Não especificado'),
                'DataOrigem': r.get('DataOrigem','Não especificado'),
                'Periodicidade': r.get('Periodicidade','Não especificado')
            })
        st.subheader('Obrigações Estruturadas')
        st.json(obr)

    # 4) Dashboard mock
    st.header('Dashboard')
    col1, col2 = st.columns(2)
    col1.metric('Total obrigações', len(df) if excel else 0)
    col2.metric('Provisionado (R$)', '180.000' if excel else '0')

elif status is False:
    st.error('Usuário ou senha inválidos')
else:
    st.warning('Digite usuário e senha')
