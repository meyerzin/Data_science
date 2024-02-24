import pandas as pd
import streamlit as st
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import time
import numpy as np


st.set_page_config(
    layout = 'wide',
    page_title = 'SETOR ECONÔMICO'
    )


st.title('\t\t:rainbow[UNA INVESTMENT - DATA SCIENCE]')
df = pd.read_excel('df_completo2.xlsx')

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

setor_escolhido = st.sidebar.radio(
    "Selecione o setor em destque: ",
    list(df_agrupado.index.values),
    index=None,horizontal=True
)

if setor_escolhido == None:
    setor_escolhido = list(df_agrupado.index.values)[0]


participacao = df['SETOR ECONÔMICO'].value_counts(normalize=True).sort_values(ascending=False)
qtde = df['SETOR ECONÔMICO'].value_counts(normalize=False).sort_values(ascending=False)[df['SETOR ECONÔMICO'].value_counts(normalize=False).sort_values(ascending=False).index == setor_escolhido].values[0]
valor = participacao[participacao.index == setor_escolhido].values[0]


st.subheader( f'{setor_escolhido} - {int(qtde / 6)} ações ({valor * 100:.2f}% participação de mercado) ')


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
        
        maior_dd = st.metric(label=f"MÁXIMO Drow down médio |  TOP {int(max_dd.rank(ascending=False)[setor_escolhido])}", 
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

######################################################################################################################################################
st.header('RENTABILIDADE ACUMULADA MÊS A MÊS POR SETOR',divider='rainbow')
st.subheader(f"RENTABILIDADE MÉDIA GERAL =  {df['RENTABILIDADE'].mean() * 100:.4f} %")
st.caption('''''')

df_perform_setores = df.groupby(['SETOR ECONÔMICO','DATA'])['ACUM_RENTABILIDADE'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SETOR ECONÔMICO').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]
if st.checkbox('ver o gráfico'):
    figura = go.Figure()
    

    h_v = st.radio('exibir dataframe da media mensal de rentabilidade acumulada por setor',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['ACUM_RENTABILIDADE']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['ACUM_RENTABILIDADE']].mean().T)

    for setor in todos_setores_econ.values:
        figura.add_trace(go.Scatter(
            x=data_1_antes, 
            y=df_perform_setores[setor].fillna(0).values * 100,
            name=setor,mode='lines+markers', text=setor, hoverinfo='text+y'
        ))

    figura.update_layout(shapes=[
                dict(
                    type='line',
                    xref='paper',
                    x0=1,
                    x1=0,
                    yref='y',
                    y0=0,
                    y1=0,
                    line=dict(color='black', width=2)
                )
            ])
    # figura.update_layout(title='Média dos retornos mensais ACUMULADOS')
    figura.update_layout(xaxis_title='DATAS', yaxis_title='RENTABILIDADE (%)')
    figura.update_layout(title='RENTABILIDADE ACUMULADA MÊS A MÊS POR SETOR ECONÔMICO')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)





st.divider()
###############################################################################################################################################
st.header('RETORNOS MENSAIS POR SETOR ECONÔMICO',divider='rainbow')

df_perform_setores = df.groupby(['SETOR ECONÔMICO','DATA'])['RETORNOS_SIMPLES'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SETOR ECONÔMICO').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]

figura = go.Figure()
st.subheader(f"MÉDIA DE RETORNO POR MÊS =  {df['RETORNOS_SIMPLES'].mean() * 100:.4f} %")
st.caption('conferir essa media depois ^^^^^^')
st.caption('''Desempenho Relativo dos Setores: Compare os retornos mensais entre diferentes setores econômicos. 
           Identifique setores que consistentemente superam ou ficam aquém do desempenho geral do mercado. 
           Isso pode indicar áreas de oportunidade ou de risco.''')
st.caption('''Sazonalidades e Padrões de Desempenho: Observe se existem padrões sazonais nos retornos mensais de determinados setores. 
           Alguns setores podem ser mais sensíveis a fatores sazonais, eventos sazonais ou mudanças climáticas.''')
st.caption('''Correlações com Indicadores Macroeconômicos: Analise se os retornos mensais têm correlação com indicadores econômicos, como taxas de juros, 
           produção industrial, emprego ou outros fatores macroeconômicos. 
           Isso pode ajudar a entender as influências externas nos setores.''')
st.caption('''Identificação de Outliers: Procure por meses em que um setor específico teve um desempenho significativamente melhor ou pior do que o esperado. 
           Isso pode indicar eventos específicos que impactaram esse setor.''')
st.caption('''Análise de Consistência: Avalie a consistência dos retornos ao longo do tempo para cada setor. 
           Setores que mantêm um desempenho estável podem ser considerados mais previsíveis.''')
if st.checkbox(' ver   gráfico    '):
    h_v = st.radio('exibir dataframe da média dos retornos mensais por setor ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['RETORNOS_SIMPLES']].mean() * 100)
    if h_v == 'HORIZONTAL':
        st.dataframe((df.groupby('SETOR ECONÔMICO')[['RETORNOS_SIMPLES']].mean() * 100).T)

    for setor in todos_setores_econ.values:
        figura.add_trace(go.Scatter(
            x=data_1_antes, 
            y=df_perform_setores[setor].fillna(0).values * 100,
            name=setor,mode='lines+markers', text=setor, hoverinfo='text+y'
        ))

    figura.update_layout(shapes=[
                dict(
                    type='line',
                    xref='paper',
                    x0=1,
                    x1=0,
                    yref='y',
                    y0=0,
                    y1=0,
                    line=dict(color='black', width=2)
                )
            ])
    # figura.update_layout(title='Média dos retornos mensais ACUMULADOS')
    figura.update_layout(xaxis_title='DATAS', yaxis_title='Retorno Mensal (%)')
    figura.update_layout(title='Retornos mensais (%) por SETOR ECONÔMICO')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)





st.divider()
########################################################################################################################################
st.header('ANÁLISE DA VOLATILIDADE MÉDIA POR SETOR',divider='rainbow')
st.subheader(f"VOLATILIDADE MÉDIA GERAL =  {df['VOLATILIDADE'].mean() * 100:.4f} %")
st.caption('''Comparação de Estabilidade Setorial: Ao observar a volatilidade média, você pode identificar setores que 
           historicamente apresentam maior estabilidade e menor flutuação nos preços das ações. 
           Isso pode indicar setores mais resilientes a choques externos.''')
st.caption('''Correlação com Eventos Econômicos: Se houver setores que mostram picos de volatilidade em momentos específicos, 
           isso pode estar relacionado a eventos econômicos, políticos ou globais. 
           Analise esses picos para entender as correlações com eventos externos.  OBSERVAR O DROWDOWN/PERGA OU GANHO BRUTO MENSAL PARA MAIS DETALHES''')
st.caption('''''')
df_graf = df.groupby('SETOR ECONÔMICO')['VOLATILIDADE'].mean() * 100
df_graf = df_graf.sort_values(ascending=False)

if st.checkbox(' ver   gráfico '):

    h_v = st.radio(' exibir tabela VOLATILIDADE média por setor   ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['VOLATILIDADE']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['VOLATILIDADE']].mean().T)

    figura = go.Figure(go.Bar(
        x=df_graf.index.values,
        y=df_graf.values,
        text=df_graf.values,  # Adicione isso se desejar que os valores apareçam nas barras
        hoverinfo='x+y',  # Isso mostra as informações de setor econômico e volatilidade ao passar o mouse
    ))
    figura.update_layout(shapes=[
        dict(
            type='line',
            xref='paper',
            x0=1,
            x1=0,
            yref='y',
            y0=0,
            y1=0,
            line=dict(color='black', width=2)
        )
    ])
    figura.update_layout(
        title='Volatilidade por Setor Econômico',
        xaxis_title='Setor Econômico',
        yaxis_title='Volatilidade (%)',
        width=1000,
        height=600,
    )
    st.plotly_chart(figura)

st.divider()
####################################################################################################################################
st.header('ANÁLISE DO GANHO/PERDA BRUTO (R$)',divider='rainbow')
st.subheader(f"PERDA/GANHO BRUTO MÉDIO GERAL =  {df['GANHO BRUTO R$'].mean():.4f} R$")
st.caption('''Desempenho Relativo dos Setores: Compare o ganho bruto acumulado entre diferentes setores ao longo do tempo.
            Identifique setores que apresentam um crescimento mais consistente em termos de ganho bruto.''')
st.caption('''Análise de Riscos: Avalie a volatilidade nos ganhos brutos acumulados para entender a 
           exposição ao risco em diferentes setores.
            Identifique os meses ou períodos de maior volatilidade e investigue as causas.''')
st.caption('''Eventos Econômicos e Impacto nos Setores:Relacione eventos econômicos significativos com as 
           mudanças nos ganhos brutos acumulados.
            Analise como eventos como crises econômicas, pandemias ou mudanças nas políticas afetam diferentes setores.''')
st.caption('''Identificação de Tendências: Observe se há tendências crescentes, decrescentes ou estáveis nos ganhos brutos acumulados para cada setor.
Analise se há padrões sazonais ou eventos específicos que afetam diferentes setores.''')
df_perform_setores = df.groupby(['SETOR ECONÔMICO','DATA'])['ACUM_GANHO BRUTO R$'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SETOR ECONÔMICO').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]

if st.checkbox(' ver gráfico'):
    figura = go.Figure()


    h_v = st.radio('exibir tabela da média (mensal) de ganho bruto por setor  ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['ACUM_GANHO BRUTO R$']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['ACUM_GANHO BRUTO R$']].mean().T)

    for setor in todos_setores_econ.values:
        figura.add_trace(go.Scatter(
            x=data_1_antes, 
            y=df_perform_setores[setor].fillna(0).values ,
            name=setor,mode='lines+markers', text=setor, hoverinfo='text+y'
        ))

    figura.update_layout(shapes=[
                dict(
                    type='line',
                    xref='paper',
                    x0=1,
                    x1=0,
                    yref='y',
                    y0=0,
                    y1=0,
                    line=dict(color='black', width=2)
                )
            ])
    # figura.update_layout(title='Média dos retornos mensais ACUMULADOS')
    figura.update_layout(xaxis_title='Período', yaxis_title='GANHO BRUTO ACUMULADO (R$)')
    figura.update_layout(title='Ganho bruto acumulado ao longo dos meses por SETOR ECONÔMICO')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)

##################################################################################################################################



st.header('ANÁLISE DO DROW DOWN (%) MÉDIO',divider='rainbow')
st.subheader(f"DROW DOWN MÉDIO GERAL =  {df['DROW_DOWN'].mean() * 100:.4f} %")


df_perform_setores = df.groupby(['SETOR ECONÔMICO','DATA'])['DROW_DOWN'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SETOR ECONÔMICO').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]
st.caption('''Resiliência do Setor: Um Drawdown Médio baixo pode indicar uma resiliência relativamente alta do setor, pois os valores negativos médios são menores. Isso sugere que, em média, as ações do setor têm experimentado quedas menores em comparação com os picos anteriores.

Volatilidade: O Drawdown Médio é uma medida da volatilidade do setor. Quanto maior o Drawdown Médio, maior a volatilidade. Isso pode influenciar as decisões de investimento, especialmente se você estiver buscando setores com menor volatilidade.

Eventos Econômicos: Picos de Drawdown podem estar associados a eventos econômicos significativos, como crises financeiras ou mudanças nas condições do mercado. Analisar os períodos de drawdown pode fornecer insights sobre os eventos que impactaram o setor.''')
if st.checkbox('ver gráfico   '):
    figura = go.Figure()

    h_v = st.radio('exibir tabela Drow Down médio mensal por setor',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['DROW_DOWN']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['DROW_DOWN']].mean().T)

    for setor in todos_setores_econ.values:
        figura.add_trace(go.Scatter(
            x=data_1_antes, 
            y=df_perform_setores[setor].fillna(0).values * 100,
            name=setor,mode='lines+markers', text=setor, hoverinfo='text+y'
        ))

    figura.update_layout(shapes=[
                dict(
                    type='line',
                    xref='paper',
                    x0=1,
                    x1=0,
                    yref='y',
                    y0=0,
                    y1=0,
                    line=dict(color='black', width=2)
                )
            ])
    # figura.update_layout(title='Média dos retornos mensais ACUMULADOS')
    figura.update_layout(xaxis_title='Período', yaxis_title='DROW DOWN (%)')
    figura.update_layout(title='Drow down médio mensal por setor econômico')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)

####################################################################################################################################

st.header('ANÁLISE DO DROW DOWN MÁXIMO (%)',divider='rainbow')
st.subheader(f"DROW DOWN MÁXIMO MÉDIO =  {df['MÁXIMO DROW DOWN'].mean() * 100:.4f} %")
st.caption('''Risco Máximo: O Drawdown Máximo fornece uma medida do risco máximo 
           enfrentado por um setor em termos de redução do valor. É a maior queda percentual em relação ao pico anterior, 
           representando o risco mais extremo experimentado pelo setor durante o período analisado.''')
st.caption('''Comparação com o Mercado: Comparar o Drawdown Máximo de um setor com o do mercado em geral 
           (índices de referência) pode ajudar a determinar se o setor é mais ou menos volátil do que o mercado em determinados momentos.''')

if st.checkbox('ver gráfico'):

    h_v = st.radio(' exibir tabela do máximo drow down por setor   ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['MÁXIMO DROW DOWN']].mean() * 100)
    if h_v == 'HORIZONTAL':
        st.dataframe((df.groupby('SETOR ECONÔMICO')[['MÁXIMO DROW DOWN']].mean() * 100).T)

    df_graf = df.groupby('SETOR ECONÔMICO')['MÁXIMO DROW DOWN'].mean() * 100
    df_graf = df_graf.sort_values(ascending=True)
    figura = go.Figure(go.Bar(
        x=df_graf.index.values,
        y=df_graf.values,
        text=df_graf.values,  # Adicione isso se desejar que os valores apareçam nas barras
        hoverinfo='x+y',  # Isso mostra as informações de setor econômico e volatilidade ao passar o mouse
    ))
    figura.update_layout(shapes=[
        dict(
            type='line',
            xref='paper',
            x0=1,
            x1=0,
            yref='y',
            y0=0,
            y1=0,
            line=dict(color='black', width=2)
        )
    ])
    figura.update_layout(
        title='Drow down máximo por setor econômico',
        xaxis_title='Setor Econômico',
        yaxis_title='DROW DOWN (%)',
        width=1000,
        height=600,
    )
    
    st.plotly_chart(figura)

st.divider()

####################################################################################################################################
st.header('ANÁLISE DA MÉDIA DOS PREÇOS DAS AÇÕES ',divider='rainbow')
st.subheader(f"PREÇO MÉDIO GERAL =  {df['PREÇO (R$)'].mean():.2f} R$")
st.caption('''Análise Setorial ou Comparativa: Comparar a média dos preços de um ativo com a média de outros ativos
            do mesmo setor ou com índices de referência pode ajudar a contextualizar o desempenho relativo.''')

st.caption('''Tendência de Longo Prazo: A média dos preços ao longo de períodos mais longos pode ajudar
             a identificar a tendência geral das ações. Uma média móvel de longo prazo suaviza flutuações de curto prazo
             e destaca a direção principal do movimento dos preços.''')
st.caption('''Análise de Regressão (Opcional):

Se desejar uma análise mais aprofundada, pode-se realizar uma análise de regressão para entender
            a relação entre a média dos preços e variáveis independentes, 
           como indicadores econômicos ou de desempenho setorial.''')


df_perform_setores = df.groupby(['SETOR ECONÔMICO','DATA'])['PREÇO (R$)'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SETOR ECONÔMICO').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]

if st.checkbox('ver grafico '):
    figura = go.Figure()

    h_v = st.radio('exibir tabela do preço médio mensal das ações  do setor    ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['MÉDIA']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SETOR ECONÔMICO')[['MÉDIA']].mean().T)

    for setor in todos_setores_econ.values:
        figura.add_trace(go.Scatter(
            x=data_1_antes, 
            y=df_perform_setores[setor].fillna(0).values,
            name=setor,mode='lines+markers', text=setor, hoverinfo='text+y'
        ))

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
    # figura.update_layout(title='Média dos retornos mensais ACUMULADOS')
    figura.update_layout(xaxis_title='Periodo', yaxis_title='Preço R$')
    figura.update_layout(title='Preço médio mensal das ações por SETOR ECONÔMICO')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)
