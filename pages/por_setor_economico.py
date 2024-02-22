import pandas as pd
import streamlit as st
from plotly import graph_objects as go
import time
import numpy as np


st.set_page_config(
    layout = 'wide',
    page_title = 'SETOR ECONÔMICO'
    )


st.title('\t\t:rainbow[UNA INVESTMENT - DATA SCIENCE]')
df = pd.read_excel('df_completo.xlsx')

st.markdown("# Análises por SETOR ECONÔMICO")
st.header('',divider='rainbow')

df_agrupado = df.groupby(by='SETOR ECONÔMICO')[['MÉDIA', 'SHARPE', 'MÁXIMO DROW DOWN', 'MÁXIMO DROW DOWN bruto',
       'VOLATILIDADE', 'RENTABILIDADE', 'GANHO BRUTO R$']].mean()

sharpe = df_agrupado['SHARPE']
media = df_agrupado['MÉDIA']
max_dd = df_agrupado['MÁXIMO DROW DOWN']
max_dd_bruto = df_agrupado['MÁXIMO DROW DOWN bruto']
volatilidade = df_agrupado['VOLATILIDADE']
rentabilidade = df_agrupado['RENTABILIDADE']
ganho_bruto = df_agrupado['GANHO BRUTO R$']

# st.dataframe(rentabilidade * 100)
# st.dataframe(ganho_bruto)
# st.dataframe(volatilidade * 100)
# st.dataframe(max_dd_bruto)
# st.dataframe(max_dd * 100)
# st.dataframe(media)
# st.dataframe(sharpe)
# st.table(pd.DataFrame(media).pivot_table(values='MÉDIA', columns='SETOR ECONÔMICO'))
setor_escolhido = st.sidebar.radio(
    "Selecione o setor em destque: ",
    list(df_agrupado.index.values),
    index=None,horizontal=True
)

if setor_escolhido == None:
    setor_escolhido = list(df_agrupado.index.values)[0]

st.subheader( setor_escolhido)


try:
    colunas_linha1 = st.columns(5)
    colunas_linha2 = st.columns(5)
    col1, col2, col3, col4, col5 = colunas_linha1
    col6, col7, col8, col9, col10 = colunas_linha2

    with col1:
        rentab = float(df_agrupado[df_agrupado.index == setor_escolhido]['RENTABILIDADE'].values)
        maior_rentabilidade = st.metric(label=f"Rentabilidade |  TOP {int(rentabilidade.rank(ascending=False)[setor_escolhido])}", 
                    value=f"{rentab * 100:.2f} %", 
                    delta=f"{(-rentabilidade.max() * 100) + (rentab * 100):.2f} % relativo ao TOP1")
        
    with col2:
        vol = float(df_agrupado[df_agrupado.index == setor_escolhido]['VOLATILIDADE'].values)
        maior_volatilidade = st.metric(label=f"Volatilidade |  TOP {int(volatilidade.rank(ascending=True)[setor_escolhido])}", 
                    value=f"{vol * 100:.2f} %", 
                    delta=f"{(-volatilidade.min() * 100) + (vol * 100):.2f} %relativo ao TOP1")

    with col3:
        ganho_brut = float(df_agrupado[df_agrupado.index == setor_escolhido]['GANHO BRUTO R$'].values)
        maior_ganho_brut = st.metric(label=f"Ganho Bruto R$ |  TOP {int(ganho_bruto.rank(ascending=False)[setor_escolhido])}", 
                    value=f"{ganho_brut :.2f} R$", 
                    delta=f"{(-ganho_bruto.max()) + (ganho_brut):.2f} R$ relativo ao TOP1")


    with col4:
        sr = float(df_agrupado[df_agrupado.index == setor_escolhido]['SHARPE'].values)
        maior_sharp_r = st.metric(label=f"Sharpe |  TOP {int(sharpe.rank(ascending=False)[setor_escolhido])}", 
                    value=f"{sr :.3f}", 
                    delta=f"{(-sharpe.max() ) + (sr ):.3f} relativo ao TOP1")

    with col7:
        dd = float(df_agrupado[df_agrupado.index == setor_escolhido]['MÁXIMO DROW DOWN'].values)
        
        maior_dd = st.metric(label=f"Drow down |  TOP {int(max_dd.rank(ascending=False)[setor_escolhido])}", 
                    value=f"{dd * 100:.3f} %", 
                    delta=f"{(-max_dd.max() * 100 ) + (dd * 100):.3f} % relativo ao TOP1")

    with col6:
        dd_bruto = float(df_agrupado[df_agrupado.index == setor_escolhido]['MÁXIMO DROW DOWN bruto'].values)
        
        maior_dd_bruto = st.metric(label=f"Perda máxima possivel|  TOP {int(max_dd_bruto.rank(ascending=False)[setor_escolhido])}", 
                    value=f"{dd_bruto :.3f} R$", 
                    delta=f"{(+max_dd_bruto.max() ) - (dd_bruto ):.3f} R$ relativo ao TOP1")

    with col5:
        medi = float(df_agrupado[df_agrupado.index == setor_escolhido]['MÉDIA'].values)
        maior_media = st.metric(label=f"Média do preço da ação |  TOP {int(media.rank(ascending=True)[setor_escolhido])}", 
                    value=f"{medi :.2f} R$", 
                    delta=f"{(-media.max()) + (medi):.2f} R$ relativo ao TOP1")
        
except:
    pass
st.divider()
st.subheader('DATAFRAMES', divider='rainbow')

visualizar_tabela = st.toggle('Vizualizar tabelas')
if visualizar_tabela:
    information = st.selectbox(
    'Informações disponíveis', ['Tabela completa', 'Por Setor', 'Por informação'])

    if information == 'Tabela completa':
        st.dataframe(df_agrupado)

    if information == 'Por Setor':
        setor = st.multiselect(
        'SETOR', list(df_agrupado.index.values))
        st.dataframe(df_agrupado.loc[df_agrupado.index.isin(setor)])
        pass
    if information == 'Por informação':
        inform = st.multiselect(
        'INFORMAÇÃO', list(df_agrupado.columns))
        st.dataframe(df_agrupado.loc[: , inform])
        # st.table(pd.DataFrame(df_agrupado[[information]]).pivot_table(values='MÉDIA', columns='SETOR ECONÔMICO'))
        pass
st.divider()
st.header('GRÁFICOS',divider='rainbow')

