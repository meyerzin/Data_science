import pandas as pd
import streamlit as st
from plotly import graph_objects as go
from plotly.subplots import make_subplots   
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

df = pd.read_excel('df_completo2.xlsx')
st.session_state["df_completo"] = df
#############################
df_precos = pd.read_excel('Case Dados - Analise de Ações.xlsx', sheet_name='PREÇOS')
df_precos_pivotada = df_precos.pivot_table(index='DATA', columns='PAPEL', values='PREÇO (R$)')

# botão mostrar tudo

st.title('\t\t:rainbow[UNA INVESTMENT - DATA SCIENCE]')
st.markdown("# Visualização geral dos dados")
st.header('',divider='rainbow')
st.subheader('Estatísticas individual')
rank = st.slider('Selecione o TOP da informação que deseja ver', min_value = 1, 
                                                            max_value = len(df['PAPEL'].unique()),
                                                            value=1)                                                                                                          # .sort_values(ascending=False).values[rank * 6]
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
    maior_rentabilidade = st.metric(label=f"RANK {rank} | Rentabilidade: {df.loc[df['RENTABILIDADE'] == df['RENTABILIDADE'].sort_values(ascending=False).values[(rank -1)* 6], 'PAPEL'].values[0]}", 
                value=f"{df['RENTABILIDADE'].sort_values(ascending=False).values[(rank - 1) * 6] * 100:.2f} %", 
                delta=f"{df.loc[df['RENTABILIDADE'] == df['RENTABILIDADE'].sort_values(ascending=False).values[(rank -1) * 6], 'GANHO BRUTO R$'].values[0]:.2f} R$ ganhos")

with col2:
    maior_rentabilidade = st.metric(label=f"RANK {rank} | Ganho bruto: {df.loc[df['GANHO BRUTO R$'] == df['GANHO BRUTO R$'].sort_values(ascending=False).values[(rank - 1) * 6],'PAPEL'].values[0]}", 
                value=f"{df['GANHO BRUTO R$'].sort_values(ascending=False).values[(rank - 1)* 6]:.2f} R$", 
                delta=f"{df.loc[df['GANHO BRUTO R$'] == df['GANHO BRUTO R$'].sort_values(ascending=False).values[(rank -1)* 6], 'RENTABILIDADE'].values[0]* 100:.2f} % de rentabilidade")

with col3:
    maior_sharpe_ratio = st.metric(label=f"RANK {rank} | Sharp Ratio: {df.loc[df['SHARPE'] == df['SHARPE'].sort_values(ascending=False).values[(rank - 1)* 6], 'PAPEL'].values[0]}",
                value = f"{df['SHARPE'].sort_values(ascending=False).values[(rank -1)* 6]:.2f}")

with col4:
    maior_dd = st.metric(label=f"RANK {rank } | Drow Down: {df.loc[df['MÁXIMO DROW DOWN'] == df['MÁXIMO DROW DOWN'].sort_values(ascending=True).values[(rank - 1) * 6], 'PAPEL'].values[0]}",
            value= f"{df['MÁXIMO DROW DOWN'].sort_values(ascending=True).values[(rank -1) * 6]* 100:.2f} %",
            delta=f"{df.loc[df['MÁXIMO DROW DOWN'] == df['MÁXIMO DROW DOWN'].sort_values(ascending=True).values[(rank- 1) * 6], 'MÁXIMO DROW DOWN bruto'].values[0]:.2f} R$ bruto")

with col5:
    maior_perda_bruta = st.metric(label=f"RANK {rank} | Perda bruta: {df.loc[df['MÁXIMO DROW DOWN bruto'] == df['MÁXIMO DROW DOWN bruto'].sort_values(ascending=True).values[(rank - 1) * 6], 'PAPEL'].values[0]}",
            value= f"{df['MÁXIMO DROW DOWN bruto'].sort_values(ascending=True).values[(rank - 1) * 6]:.2f} R$",
            delta=f"{df.loc[df['MÁXIMO DROW DOWN bruto'] == df['MÁXIMO DROW DOWN bruto'].sort_values(ascending=True).values[(rank - 1)* 6], 'MÁXIMO DROW DOWN'].values[0] * 100:.2f} % rentabilidade")

st.caption('INFORMAÇÕES DE VARIAÇÃO SÃO RELATIVAS A PRÓPRIA AÇÃO OBSERVADA')

st.subheader(F'Estatísticas TOTAIS das {len(df.PAPEL.unique())} ações')
col1, col2, col3, col4 = st.columns(4)
with col1:
    maior_rentabilidade = st.metric(label=f" VARIAÇÃO(%) NO PREÇO TOTAL EM 6 MESES", 
                value=f"{(df.groupby('DATA')['PREÇO (R$)'].sum().iloc[-1] / df.groupby('DATA')['PREÇO (R$)'].sum().iloc[0] - 1) * 100:.3f} %", 
                delta=f"")

with col2:
    maior_rentabilidade = st.metric(label=f" VARAIÇÃO(R$) NO PREÇO TOTAL 6 MESES", 
                value=f"{(df.groupby('DATA')['PREÇO (R$)'].sum().iloc[-1] - df.groupby('DATA')['PREÇO (R$)'].sum().iloc[0]):.3f} R$", 
                delta=f"")
    
with col3:
    maior_rentabilidade = st.metric(label=f"VOLATILIDADE MÉDIA NO PERÍODO", 
            value= f"{df.VOLATILIDADE.mean() * 100:.3f} %",
            delta=f"")

with col4:
    maior_dd = st.metric(label=f"RENTABILIDADE MÉDIA NO PERÍODO",
            value= f"{df.RENTABILIDADE.mean() * 100:.3f} %",
            delta=f"")


st.divider()
st.subheader('DATAFRAMES', divider='rainbow')
st.caption('selecionar na direita informações que quer observar ou ver tudo.')

mostrar_todos = st.checkbox("Mostrar todos os dados")
if mostrar_todos:
    filtro_acao = st.checkbox("Filtrar por ação")
    
    if filtro_acao:
        st.caption('SELECIONAR AS AÇÕES NA ABA DO LADO À ESQUERDA')
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
    if mostrar_filtro_coluna:
        df_filtrado_set_econ = df[df['SETOR ECONÔMICO'] == setor_economico][filtrar_colunas]
    st.dataframe(df_filtrado_set_econ)

#botao filtrar df SUBSETOR
mostrar_subsetores = st.checkbox('Selecionar dados por: SUBSETORES')
if mostrar_subsetores:
    subsetores = df['SUBSETOR'].value_counts().index
    subsetor = st.selectbox('Subsetores', subsetores)
    df_filtrado_subsetores = df[df['SUBSETOR'] == subsetor]
    if mostrar_filtro_coluna:
        df_filtrado_subsetores = df[df['SUBSETOR'] == subsetor][filtrar_colunas]
    st.dataframe(df_filtrado_subsetores)

#botao filtrar df SEGMENTO
mostrar_segmentos = st.checkbox('Selecionar dados por: SEGMENTO')
if mostrar_segmentos:
    segmentos = df['SEGMENTO'].value_counts().index
    segmento = st.selectbox('Segmento', segmentos)
    df_filtrado_segmento = df[df['SEGMENTO'] == segmento]
    if mostrar_filtro_coluna:
        df_filtrado_segmento = df[df['SEGMENTO'] == segmento][filtrar_colunas]
    st.dataframe(df_filtrado_segmento)

# st.divider()

# st.header('MULTI SELECIONADOR DE DADOS', divider='rainbow')
st.subheader('MULTI SELECIONADOR DE DADOS')

setores_economicos = df['SETOR ECONÔMICO'].value_counts().index
setor_economico = st.selectbox('Setores econômicos', setores_economicos)
df_filtrado = df[df['SETOR ECONÔMICO'] == setor_economico]

subsetores = df_filtrado['SUBSETOR'].value_counts().index
subsetor = st.selectbox('Subsetores', subsetores)


df_filtrado2 = df[df['SUBSETOR'] == subsetor]
display = st.checkbox('Display multi-selector data')

st.divider()

if display:
    if mostrar_filtro_coluna:
        df_filtrado2 = df[df['SUBSETOR'] == subsetor][filtrar_colunas]
    st.dataframe(df_filtrado2)


# st.header('GRÁFICO DA PERFORMANCE DAS AÇÕES AO LONGO DOS ANOS', divider='rainbow')
st.subheader('GRÁFICO DA PERFORMANCE DAS AO LONGO DOS ANOS', divider='rainbow')
number = st.number_input('Quantidade de ações para ver', min_value=1, max_value=25,value=10)

_LOREM_IPSUM = """
Vizualizando os Gráficos de performance das ações ao longo dos anos. 
"""


def stream_data():
    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.02)

    

    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.02)


if st.toggle(f":red[Gráfico das ações que PIOR performaram (TOP{number}) - (rentabilidade <= 1)]"):
    st.write_stream(stream_data)

    df_precos = pd.read_excel('Case Dados - Analise de Ações.xlsx', sheet_name='PREÇOS')
    df_precos_pivotada = df_precos.pivot_table(index='DATA', columns='PAPEL', values='PREÇO (R$)')

    df_precos_pivotada_normalizada = df_precos_pivotada / df_precos_pivotada.iloc[0]

    ret_menores_que_1 = df_precos_pivotada_normalizada.loc[:, df_precos_pivotada_normalizada.loc[df_precos_pivotada_normalizada.index[-1]] <= 1]

    figura = go.Figure()

    for col in ret_menores_que_1.iloc[-1].sort_values(ascending=True)[0:number].index:
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

if st.toggle(f":green[Gráfico das ações que MELHOR performaram (TOP{number}) - (rentabilidade >= 1)]"):
    st.write_stream(stream_data)

    df_precos = pd.read_excel('Case Dados - Analise de Ações.xlsx', sheet_name='PREÇOS')
    df_precos_pivotada = df_precos.pivot_table(index='DATA', columns='PAPEL', values='PREÇO (R$)')

    df_precos_pivotada_normalizada = df_precos_pivotada / df_precos_pivotada.iloc[0]

    ret_maiores_que_1 = df_precos_pivotada_normalizada.loc[:, df_precos_pivotada_normalizada.loc[df_precos_pivotada_normalizada.index[-1]] >= 1]

    figura = go.Figure()

    for col in ret_maiores_que_1.iloc[-1].sort_values(ascending=False)[0:number].index:
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

st.header('GRAFICOS:  COMPARATIVO INDIVIDUAL -----> MELHOR PERFORMANCE',divider='rainbow')

if st.checkbox('exibir graficos comparativos'):
    stock_compare_choose = st.radio('escolha a ação',df[['NOME']].drop_duplicates(), horizontal=True)

    varias_acoes = st.multiselect('escolha mais de uma ação', df[['NOME']].drop_duplicates())



    # GRAFICO BARRAS
    # GRAFICO BARRAS
    # GRAFICO BARRAS
    st.header('SHARP RATIOS', divider='rainbow')
    if st.toggle('visualizar grafico sharpe ratio'):
        if varias_acoes:
            sharpe_max = df.loc[df['SHARPE'] == df['SHARPE'].max(), ['NOME','SHARPE']]
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['SHARP RATIOS'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            
            for nome_acao in varias_acoes:
                # figura.add_trace(go.Bar(x=nome_acao, y=df['SHARPE'].loc[df['NOME'] == nome_acao].values[0], name=nome_acao), row=1, col=1)
                figura.add_trace(go.Bar(y=[nome_acao], x=[df['SHARPE'].loc[df['NOME'] == nome_acao].values[0]], name=nome_acao,
                orientation='h',text=[nome_acao],hoverinfo='x+text'))
            figura.update_layout(shapes=[
                dict(
                    type='line',
                    yref='paper',
                    y0=0,
                    y1=1,
                    xref='x',
                    x0=0,
                    x1=0,
                    line=dict(color='white', width=2)
                )
            ])
            figura.add_trace(go.Bar(y=['Máximo Sharpe'], x=[sharpe_max['SHARPE'].values[0]], name=sharpe_max['NOME'].values[0],
            orientation='h',text=sharpe_max['NOME'].values[0],hoverinfo='x+text'))
            # figura.add_trace(go.Bar(x=df['NOME'].unique(), y=sharpe_max['SHARPE'].unique(), 
            #                         name=sharpe_max['NOME'].unique()[0]), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
        else:
            sharpe_max = df.loc[df['SHARPE'] == df['SHARPE'].max(), ['NOME','SHARPE']]
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['SHARP RATIOS'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            
            for nome_acao in [stock_compare_choose]:
                # figura.add_trace(go.Bar(x=nome_acao, y=df['SHARPE'].loc[df['NOME'] == nome_acao].values[0], name=nome_acao), row=1, col=1)
                figura.add_trace(go.Bar(y=[nome_acao], x=[df['SHARPE'].loc[df['NOME'] == nome_acao].values[0]], name=nome_acao,
                orientation='h',text=[nome_acao],hoverinfo='x+text'))

            figura.update_layout(shapes=[
                dict(
                    type='line',
                    yref='paper',
                    y0=0,
                    y1=1,
                    xref='x',
                    x0=0,
                    x1=0,
                    line=dict(color='white', width=2)
                )
            ])
            figura.add_trace(go.Bar(y=['Máximo Sharpe'], x=[sharpe_max['SHARPE'].values[0]], name=sharpe_max['NOME'].values[0],
            orientation='h',text=sharpe_max['NOME'].values[0],hoverinfo='x+text'))
            # figura.add_trace(go.Bar(x=df['NOME'].unique(), y=sharpe_max['SHARPE'].unique(), 
            #                         name=sharpe_max['NOME'].unique()[0]), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
    # RENTABILIDADE GRAFICO:
    # RENTABILIDADE GRAFICO:
    # RENTABILIDADE GRAFICO:
    st.divider()
    st.header('RETORNOS MENSAIS', divider='rainbow')
    if st.toggle('visualizar grafico retornos mensais'):
        if varias_acoes:
            rent_max = df.loc[df['RENTABILIDADE'] == df['RENTABILIDADE'].max(), ['NOME','RETORNOS_SIMPLES']]
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['RENTABILIDADE MENSAL'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            
            for nome_acao in varias_acoes:
                figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=df['RETORNOS_SIMPLES'].loc[df['NOME'] == nome_acao].fillna(0), name=nome_acao), row=1, col=1)
            
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=[0] * 6,name='zero',mode='lines',line=dict(color='white')), row=1, col=1)
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=rent_max['RETORNOS_SIMPLES'].fillna(0), 
                                    name=rent_max['NOME'].unique()[0],line=dict(color='#00FF00')), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
        else:
            rent_max = df.loc[df['RENTABILIDADE'] == df['RENTABILIDADE'].max(), ['NOME','RETORNOS_SIMPLES']]
            
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['RETORNOS MENSAIS'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            for nome_acao in [stock_compare_choose]:
                figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=df['RETORNOS_SIMPLES'].loc[df['NOME'] == stock_compare_choose].fillna(0), name=stock_compare_choose), row=1, col=1)
            
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=[0] * 6,name='zero',mode='lines',line=dict(color='red')), row=1, col=1)
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=rent_max['RETORNOS_SIMPLES'].fillna(0), 
                                    name=rent_max['NOME'].unique()[0],line=dict(color='#00FF00')), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
    st.divider()

    # RENTABILIDADE ACUMULADA GRAFICO:
    # RENTABILIDADE ACUMULADA GRAFICO:
    # RENTABILIDADE ACUMULADA GRAFICO:
    st.header('RENTABILIDADE MENSAL ACUMULADA', divider='rainbow')
    if st.toggle('visualizar grafico rentabilidade'):
        if varias_acoes:
            rent_max = df.loc[df['RENTABILIDADE'] == df['RENTABILIDADE'].max(), ['NOME','ACUM_RENTABILIDADE']]
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['RENTABILIDADE MENSAL ACUMULADA'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            
            for nome_acao in varias_acoes:
                figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=df['ACUM_RENTABILIDADE'].loc[df['NOME'] == nome_acao].fillna(0), name=nome_acao), row=1, col=1)
            
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=[0] * 6,name='zero',mode='lines',line=dict(color='white')), row=1, col=1)
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=rent_max['ACUM_RENTABILIDADE'].fillna(0), 
                                    name=rent_max['NOME'].unique()[0],line=dict(color='#00FF00')), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
        else:
            rent_max = df.loc[df['RENTABILIDADE'] == df['RENTABILIDADE'].max(), ['NOME','ACUM_RENTABILIDADE']]
            
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['RENTABILIDADE MENSAL ACUMULADA'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            for nome_acao in [stock_compare_choose]:
                figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=df['ACUM_RENTABILIDADE'].loc[df['NOME'] == stock_compare_choose].fillna(0), name=stock_compare_choose), row=1, col=1)
            
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=[0] * 6,name='zero',mode='lines',line=dict(color='red')), row=1, col=1)
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=rent_max['ACUM_RENTABILIDADE'].fillna(0), 
                                    name=rent_max['NOME'].unique()[0],line=dict(color='#00FF00')), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
    st.divider()


    # RENTABILIDADE GANHO / PERDA BRUTA:
    # RENTABILIDADE GANHO / PERDA BRUTA:
    # RENTABILIDADE GANHO / PERDA BRUTA:
    st.header('ACUMULADO DE GANHO OU PERDA BRUTO R$', divider='rainbow')
    if st.toggle('visualizar grafico perda/ganho R$'):
        if varias_acoes:
            rent_max = df.loc[df['GANHO BRUTO R$'] == df['GANHO BRUTO R$'].max(), ['NOME','ACUM_GANHO BRUTO R$']]
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['ACUMULADO DE GANHO OU PERDA BRUTA R$'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            
            for nome_acao in varias_acoes:
                figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=df['ACUM_GANHO BRUTO R$'].loc[df['NOME'] == nome_acao].fillna(0), name=nome_acao), row=1, col=1)
            
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=[0] * 6,name='zero',mode='lines',line=dict(color='white')), row=1, col=1)
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=rent_max['ACUM_GANHO BRUTO R$'].fillna(0), 
                                    name=rent_max['NOME'].unique()[0],line=dict(color='#00FF00')), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
        else:
            rent_max = df.loc[df['GANHO BRUTO R$'] == df['GANHO BRUTO R$'].max(), ['NOME','ACUM_GANHO BRUTO R$']]
            
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['ACUMUMULADO DE GANHO OU PERDA BRUTA R$'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            for nome_acao in [stock_compare_choose]:
                figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=df['ACUM_GANHO BRUTO R$'].loc[df['NOME'] == stock_compare_choose].fillna(0), name=stock_compare_choose), row=1, col=1)
            
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=[0] * 6,name='zero',mode='lines',line=dict(color='red')), row=1, col=1)
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=rent_max['ACUM_GANHO BRUTO R$'].fillna(0), 
                                    name=rent_max['NOME'].unique()[0],line=dict(color='#00FF00')), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
    st.divider()


    # DROW DOWN:
    # DROW DOWN:
    # DROW DOWN:
    st.header('DROW DOWNS', divider='rainbow')
    if st.toggle('visualizar grafico draw down'):
        if varias_acoes:
            rent_max = df.loc[df['MÁXIMO DROW DOWN'] == df['MÁXIMO DROW DOWN'].max(), ['NOME','DROW_DOWN']]
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['DROW DOWNS'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            
            for nome_acao in varias_acoes:
                figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=df['DROW_DOWN'].loc[df['NOME'] == nome_acao].fillna(0), name=nome_acao), row=1, col=1)
            
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=[0] * 6,name='zero',mode='lines',line=dict(color='white')), row=1, col=1)
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=rent_max['DROW_DOWN'].fillna(0), 
                                    name=rent_max['NOME'].unique()[0],line=dict(color='#00FF00')), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)
        else:
            rent_max = df.loc[df['MÁXIMO DROW DOWN'] == df['MÁXIMO DROW DOWN'].max(), ['NOME','DROW_DOWN']]
            
            figura = make_subplots(rows = 1, cols=1, subplot_titles=['DROW DOWNS'])#, 'RENTABILIDADE ACUMULADA', 'GANHO BRUTO ACUMULADO', 'DROW DOWN'])
            for nome_acao in [stock_compare_choose]:
                figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=df['DROW_DOWN'].loc[df['NOME'] == stock_compare_choose].fillna(0), name=stock_compare_choose), row=1, col=1)
            
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=[0] * 6,name='zero',mode='lines',line=dict(color='red')), row=1, col=1)
            figura.add_trace(go.Scatter(x=df['DATA'].unique(), y=rent_max['DROW_DOWN'].fillna(0), 
                                    name=rent_max['NOME'].unique()[0],line=dict(color='#00FF00')), row=1, col=1)
            figura.update_layout(width=1100,height=700)
            st.plotly_chart(figura)



st.divider()



st.header('"sazonalidade" / evento disruptivo', divider='rainbow')


st.caption('analise por mes, para ver se teve algum mês que pode ter tido um evento que fez com que todas ações caissem, ou se tem algum tipo de sazonalidade de certa forma')


if st.checkbox('mostrar'):

    from dateutil.relativedelta import relativedelta
    import datetime
    st.subheader('média DA RENTABILIDADE das ações',divider='rainbow')
    _ = df.groupby('DATA')['RETORNOS_ACUMULADOS'].mean().sort_index().fillna(0) * 100
    col1,col2 = st.columns([0.6,0.3])
    with col1:
        figura = go.Figure()   
        data_1_antes = [data - relativedelta(months=1) for data in _.index]        
        figura.add_trace(go.Scatter(x=data_1_antes, y=_.values, mode='lines+markers', text=_.index, hoverinfo='x+y', name='DATA'))

        figura.update_layout(shapes=[
            dict(
                type='line',
                xref='paper',
                x0=1,
                x1=0,
                yref='y',
                y0=0,
                y1=0,
                line=dict(color='white', width=2)
            )
        ])
        figura.update_layout(title='Média dos retornos mensais ACUMULADOS')
        figura.update_layout(xaxis_title='DATAS', yaxis_title='Retorno Mensal ACUMULADO (%)')

        figura.update_layout(width=700, height=550)
        st.plotly_chart(figura)
    with col2:
        st.dataframe(df[['DATA','RETORNOS_ACUMULADOS']].groupby('DATA').mean() * 100)

    st.divider()


    st.subheader('média dos retornos mensais das ações',divider='rainbow')

    _ = df.groupby('DATA')['RETORNOS_SIMPLES'].mean().sort_index().fillna(0) * 100

    col1,col2 = st.columns([0.6,0.3])
    with col1:
        figura = go.Figure()   
        data_1_antes = [data - relativedelta(months=1) for data in _.index]        
        figura.add_trace(go.Bar(x=data_1_antes, y=_.values, orientation='v', text=_.index, hoverinfo='x+y', name='DATA'))

        figura.update_layout(shapes=[
            dict(
                type='line',
                xref='paper',
                x0=1,
                x1=0,
                yref='y',
                y0=0,
                y1=0,
                line=dict(color='white', width=2)
            )
        ])
        figura.update_layout(title='Média dos retornos mensais')
        figura.update_layout(xaxis_title='DATAS', yaxis_title='retorno mensal - (%)')
        
        figura.update_layout(width=700, height=550)
        st.plotly_chart(figura) 
    with col2:
        st.dataframe(df[['DATA','RETORNOS_SIMPLES']].groupby('DATA').mean() * 100)

    st.divider()

    st.subheader('média dos ganhos/perdas brutos das ações ao longo dos meses',divider='rainbow')
    col1,col2 = st.columns([0.6,0.3])

    # st.dataframe(df[['DATA','ACUM_GANHO BRUTO R$']].pct_change().groupby('DATA').mean())

    _ = df.groupby('DATA')['ACUM_GANHO BRUTO R$'].mean().sort_index().fillna(0)

    col1,col2 = st.columns([0.6,0.3])
    with col1:
        figura = go.Figure()   
        data_1_antes = [data - relativedelta(months=1) for data in _.index]        
        figura.add_trace(go.Bar(x=data_1_antes, y=_.values, orientation='v', text=_.index, hoverinfo='x+y', name='DATA'))

        figura.update_layout(shapes=[
            dict(
                type='line',
                xref='paper',
                x0=1,
                x1=0,
                yref='y',
                y0=0,
                y1=0,
                line=dict(color='white', width=2)
            )
        ])
        figura.update_layout(title='Média dos ganhos/perdas')
        figura.update_layout(xaxis_title='DATAS', yaxis_title='perda/ganho médio - (R$)')
        figura.update_layout(width=700, height=550)
        st.plotly_chart(figura) 
    with col2:
        st.dataframe(df[['DATA','ACUM_GANHO BRUTO R$']].groupby('DATA').mean())

    