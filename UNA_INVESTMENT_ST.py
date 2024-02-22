import pandas as pd
import streamlit as st
from plotly import graph_objects as go
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    layout = 'wide',
    page_title = 'Una INVESTMENT - Data Science'
    )

##############
@st.cache_data
def load_df():
    df = pd.read_excel('df_completo.xlsx')
    return df

df = pd.read_excel('df_completo.xlsx')
st.session_state["df_completo"] = df
#############################
df_precos = pd.read_excel('Case Dados - Analise de Ações.xlsx', sheet_name='PREÇOS')
df_precos_pivotada = df_precos.pivot_table(index='DATA', columns='PAPEL', values='PREÇO (R$)')

# botão mostrar tudo

st.title('\t\t:rainbow[UNA INVESTMENT - DATA SCIENCE]')
st.markdown("# Visualização geral dos dados")
st.header('',divider='rainbow')   

rank = st.slider('Selecione o rank da ação que deseja ver', min_value = 0, 
                                                            max_value = len(df['PAPEL'].unique()) - 1,
                                                            value=0)

                                                                                                          # .sort_values(ascending=False).values[rank * 6]
##########################################################
mostrar_filtro_coluna = st.sidebar.checkbox("Filtrar informacoes")
if mostrar_filtro_coluna:         
    filtrar_colunas = st.sidebar.multiselect(
        "Quais informações deseja visualizar?",
        df.columns,
        default=None)

##########################################
                                                                                                    # .sort_values(ascending=True).values[rank * 6]
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    maior_rentabilidade = st.metric(label=f"RANK {rank + 1} | Rentabilidade: {df.loc[df['RENTABILIDADE'] == df['RENTABILIDADE'].sort_values(ascending=False).values[rank * 6], 'PAPEL'].values[0]}", 
                value=f"{df['RENTABILIDADE'].sort_values(ascending=False).values[rank * 6] * 100:.2f} %", 
                delta=f"{df.loc[df['RENTABILIDADE'] == df['RENTABILIDADE'].sort_values(ascending=False).values[rank * 6], 'GANHO BRUTO R$'].values[0]:.2f} R$ ganhos")

with col2:
    maior_rentabilidade = st.metric(label=f"RANK {rank + 1} | Ganho bruto: {df.loc[df['GANHO BRUTO R$'] == df['GANHO BRUTO R$'].sort_values(ascending=False).values[rank * 6],'PAPEL'].values[0]}", 
                value=f"{df['GANHO BRUTO R$'].sort_values(ascending=False).values[rank * 6]:.2f} R$", 
                delta=f"{df.loc[df['GANHO BRUTO R$'] == df['GANHO BRUTO R$'].sort_values(ascending=False).values[rank * 6], 'RENTABILIDADE'].values[0]* 100:.2f} % rentabilidade")

with col3:
    maior_sharpe_ratio = st.metric(label=f"RANK {rank+ 1} | Sharp Ratio: {df.loc[df['SHARPE'] == df['SHARPE'].sort_values(ascending=False).values[rank * 6], 'PAPEL'].values[0]}",
                value = f"{df['SHARPE'].sort_values(ascending=False).values[rank * 6]:.2f}")

with col4:
    maior_dd = st.metric(label=f"RANK {rank + 1} | Drow Down: {df.loc[df['MÁXIMO DROW DOWN'] == df['MÁXIMO DROW DOWN'].sort_values(ascending=True).values[rank * 6], 'PAPEL'].values[0]}",
            value= f"{df['MÁXIMO DROW DOWN'].sort_values(ascending=True).values[rank * 6]* 100:.2f} %",
            delta=f"{df.loc[df['MÁXIMO DROW DOWN'] == df['MÁXIMO DROW DOWN'].sort_values(ascending=True).values[rank * 6], 'MÁXIMO DROW DOWN bruto'].values[0]:.2f} R$ bruto")

with col5:
    maior_perda_bruta = st.metric(label=f"RANK {rank+ 1} | Perda bruta: {df.loc[df['MÁXIMO DROW DOWN bruto'] == df['MÁXIMO DROW DOWN bruto'].sort_values(ascending=True).values[rank * 6], 'PAPEL'].values[0]}",
            value= f"{df['MÁXIMO DROW DOWN bruto'].sort_values(ascending=True).values[rank * 6]:.2f} R$",
            delta=f"{df.loc[df['MÁXIMO DROW DOWN bruto'] == df['MÁXIMO DROW DOWN bruto'].sort_values(ascending=True).values[rank * 6], 'MÁXIMO DROW DOWN'].values[0] * 100:.2f} % rentabilidade")
st.caption('INFORMAÇÕES RELATIVAS A PRÓPRIA AÇÃO')
st.divider()
st.subheader('DATAFRAMES', divider='rainbow')

mostrar_todos = st.checkbox("Mostrar todos os dados")
if mostrar_todos:
    filtro_acao = st.checkbox("Filtrar por ação")
    if filtro_acao:
        st.sidebar.divider()
        acoes_selecionadas = st.sidebar.multiselect(
        "Quais ações deseja visualizar?",
        df_precos_pivotada.columns,
        default=None,
        key="acoes")

        try:
            st.dataframe(df[filtrar_colunas].loc[df['PAPEL'].isin(acoes_selecionadas)])
        except:
            st.dataframe(df.loc[df['PAPEL'].isin(acoes_selecionadas)])

        # grafico_barras = st.button("mostrar grafico de barras")

        # tickers = ['ABEV3', 'YDUQ3','AZUL4']
        # best_tickers = df.loc[: , ['MÉDIA' ,'SHARPE', 'MÁXIMO DROW DOWN', 'MÁXIMO DROW DOWN bruto', 'VOLATILIDADE', 'RENTABILIDADE', 'GANHO BRUTO R$']].idxmax().values

        # max_values = df.loc[: , ['MÉDIA' ,'SHARPE', 'MÁXIMO DROW DOWN', 'MÁXIMO DROW DOWN bruto', 'VOLATILIDADE', 'RENTABILIDADE', 'GANHO BRUTO R$']].max().values
        # info = df.loc[: , ['MÉDIA' ,'SHARPE', 'MÁXIMO DROW DOWN', 'MÁXIMO DROW DOWN bruto', 'VOLATILIDADE', 'RENTABILIDADE', 'GANHO BRUTO R$']].max().index.values

        # if grafico_barras:
        #     acoes_selecionadas
        #     info
        #     figura = go.Figure()

        #     # Adiciona barras para cada indicador
        #     for acao in acoes_selecionadas:
        #         figura.add_trace(go.Bar(name=acao, x=info, 
        #                                 y=round(df.loc[df.index == acao, info],2),
        #                                 marker_color='blue',)
        #                                 )
                
                
        #     # Layout do gráfico
        #     figura.update_layout(barmode='group', title='Valores Máximos por Indicador e Ação',
        #                         xaxis_title='Informações', yaxis_title='Valor',)
        #     st.plotly_chart(figura)







        st.divider()
    else:
        try:
            filtrar_colunas
            if len(filtrar_colunas) < 1 or not filtrar_colunas:
                st.dataframe(df)
            else:
                st.dataframe(df[filtrar_colunas])
        except:
            st.dataframe(df)

        st.divider()


#botao filtrar df SETOR ECONOMICO
mostrar_set_econ = st.checkbox('Selecionar dados por: SETORES ECONÔMICOS')
if mostrar_set_econ:
    setores_economicos = df['SETOR ECONÔMICO'].value_counts().index
    setor_economico = st.selectbox('Setores Econômicos', setores_economicos)
    df_filtrado_set_econ = df[df['SETOR ECONÔMICO'] == setor_economico]
    st.dataframe(df_filtrado_set_econ)

#botao filtrar df SUBSETOR
mostrar_subsetores = st.checkbox('Selecionar dados por: SUBSETORES')
if mostrar_subsetores:
    subsetores = df['SUBSETOR'].value_counts().index
    subsetor = st.selectbox('Subsetores', subsetores)
    df_filtrado_subsetores = df[df['SUBSETOR'] == subsetor]
    st.dataframe(df_filtrado_subsetores)

#botao filtrar df SEGMENTO
mostrar_segmentos = st.checkbox('Selecionar dados por: SEGMENTO')
if mostrar_segmentos:
    segmentos = df['SEGMENTO'].value_counts().index
    segmento = st.selectbox('Segmento', segmentos)
    df_filtrado_segmento = df[df['SEGMENTO'] == segmento]
    st.dataframe(df_filtrado_segmento)

st.divider()

# st.header('MULTI SELECIONADOR DE DADOS', divider='rainbow')
st.subheader('MULTI SELECIONADOR DE DADOS', divider='rainbow')

setores_economicos = df['SETOR ECONÔMICO'].value_counts().index
setor_economico = st.selectbox('Setores Econômicos', setores_economicos)
df_filtrado = df[df['SETOR ECONÔMICO'] == setor_economico]

subsetores = df_filtrado['SUBSETOR'].value_counts().index
subsetor = st.selectbox('Subsetores', subsetores)


df_filtrado2 = df[df['SUBSETOR'] == subsetor]
display = st.checkbox('Display multi-selector data')

st.divider()

if display:
    st.dataframe(df_filtrado2)


# st.header('GRÁFICO DA PERFORMANCE DAS AÇÕES AO LONGO DOS ANOS', divider='rainbow')
st.subheader('GRÁFICO DA PERFORMANCE DAS :red[MELHORES AÇÕES] AO LONGO DOS ANOS', divider='rainbow')


_LOREM_IPSUM = """
Vizualizando os Gráficos de perfoemance das ações ao longo dos anos. 
"""


def stream_data():
    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.02)

    

    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.02)


if st.toggle("Gráfico das ações que PIOR performaram TOP(10) - (rentabilidade <= 1)"):
    st.write_stream(stream_data)

    df_precos = pd.read_excel('Case Dados - Analise de Ações.xlsx', sheet_name='PREÇOS')
    df_precos_pivotada = df_precos.pivot_table(index='DATA', columns='PAPEL', values='PREÇO (R$)')

    df_precos_pivotada_normalizada = df_precos_pivotada / df_precos_pivotada.iloc[0]

    ret_menores_que_1 = df_precos_pivotada_normalizada.loc[:, df_precos_pivotada_normalizada.loc[df_precos_pivotada_normalizada.index[-1]] <= 1]

    figura = go.Figure()

    for col in ret_menores_que_1.iloc[-1].sort_values(ascending=True)[0:10].index:
        trace = go.Scatter(x=ret_menores_que_1.index, y=ret_menores_que_1[col] - 1, mode='lines+markers', name=col)
        figura.add_trace(trace)

    figura.update_layout(title='Evolução do Preço das Ações ao Longo do Tempo COM RENTABILIDADE RUIM')
    figura.update_layout(legend_title_text='TICKER')

    figura.update_layout(
        title='Evolução do Preço das Ações ao Longo do Tempo',
        legend_title_text='TICKER',
        xaxis_title='Data',
        yaxis_title='Preço',
        height=700,
        width = 1100
    )

    st.plotly_chart(figura)

if st.toggle("Gráfico das ações que MELHOR performaram (TOP10) - (rentabilidade >= 1)"):
    st.write_stream(stream_data)

    df_precos = pd.read_excel('Case Dados - Analise de Ações.xlsx', sheet_name='PREÇOS')
    df_precos_pivotada = df_precos.pivot_table(index='DATA', columns='PAPEL', values='PREÇO (R$)')

    df_precos_pivotada_normalizada = df_precos_pivotada / df_precos_pivotada.iloc[0]

    ret_maiores_que_1 = df_precos_pivotada_normalizada.loc[:, df_precos_pivotada_normalizada.loc[df_precos_pivotada_normalizada.index[-1]] >= 1]

    figura = go.Figure()

    for col in ret_maiores_que_1.iloc[-1].sort_values(ascending=False)[0:10].index:
        trace = go.Scatter(x=ret_maiores_que_1.index, y=ret_maiores_que_1[col], mode='lines+markers', name=col)
        figura.add_trace(trace)

    figura.update_layout(title='Evolução do Preço das Ações ao Longo do Tempo COM RENTABILIDADE RUIM')
    figura.update_layout(legend_title_text='TICKER')

    figura.update_layout(
        title='Evolução do Preço das Ações ao Longo do Tempo',
        legend_title_text='TICKER',
        xaxis_title='Data',
        yaxis_title='Preço',
        height=700,
        width=1100
    )

    st.plotly_chart(figura)

st.divider()













# with st.sidebar:
#     with st.echo():
#         st.write("This code will be printed to the sidebar.")

#     with st.spinner("Loading..."):
#         time.sleep(5)
#     st.success("Done!")

# # Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

# # Using "with" notation
# with st.sidebar:
#     add_radio = st.radio(
#         "Choose a shipping method",
#         ("Standard (5-15 days)", "Express (2-5 days)")
#     )

    