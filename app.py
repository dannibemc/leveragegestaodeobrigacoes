import streamlit as st
import streamlit_authenticator as stauth
import yaml
import pandas as pd

# Carrega credenciais
with open('config.yaml') as f:
    config = yaml.safe_load(f)

auth = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, status, username = auth.login('Login', 'main')

if status:
    auth.logout('Logout', 'main')
    st.write(f'Olá, **{name}**')
    st.title('Leverage - Gestão de Obrigações')

    # Upload de obrigações
    excel = st.file_uploader('Selecione .xlsx', type=['xlsx'])
    if excel:
        df = pd.read_excel(excel)
        st.dataframe(df)

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
        st.json(obr)

elif status is False:
    st.error('Usuário ou senha inválidos')
else:
    st.warning('Digite usuário e senha')
