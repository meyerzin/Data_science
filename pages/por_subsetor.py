import pandas as pd
import streamlit as st
from plotly import graph_objects as go
import time
import numpy as np


st.set_page_config(
    layout = 'wide',
    page_title = 'SUBSETOR'
    )


st.title('\t\t:rainbow[UNA INVESTMENT - DATA SCIENCE]')
df = pd.read_excel('df_completo2.xlsx')

st.markdown("# Análises por SUBSETOR")
st.header('',divider='rainbow')

df_agrupado = df.groupby(by='SUBSETOR')[['MÉDIA', 'SHARPE', 'MÁXIMO DROW DOWN', 'MÁXIMO DROW DOWN bruto',
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
# st.table(pd.DataFrame(media).pivot_table(values='MÉDIA', columns='SUBSETOR'))
subsetor_escolhido = st.sidebar.radio(
    "Selecione o subsetor em destque: ",
    list(df_agrupado.index.values),
    index=None,horizontal=True
)

if subsetor_escolhido == None:
    subsetor_escolhido = list(df_agrupado.index.values)[0]

st.subheader( subsetor_escolhido)


try:
    colunas_linha1 = st.columns(5)
    colunas_linha2 = st.columns(5)
    col1, col2, col3, col4, col5 = colunas_linha1
    col6, col7, col8, col9, col10 = colunas_linha2

    with col1:
        rentab = float(df_agrupado[df_agrupado.index == subsetor_escolhido]['RENTABILIDADE'].values)
        maior_rentabilidade = st.metric(label=f"Rentabilidade |  TOP {int(rentabilidade.rank(ascending=False)[subsetor_escolhido])}", 
                    value=f"{rentab * 100:.2f} %", 
                    delta=f"{(-rentabilidade.max() * 100) + (rentab * 100):.2f} % relativo ao TOP1")
        
    with col2:
        vol = float(df_agrupado[df_agrupado.index == subsetor_escolhido]['VOLATILIDADE'].values)
        maior_volatilidade = st.metric(label=f"Volatilidade |  TOP {int(volatilidade.rank(ascending=True)[subsetor_escolhido])}", 
                    value=f"{vol * 100:.2f} %", 
                    delta=f"{(-volatilidade.min() * 100) + (vol * 100):.2f} %relativo ao TOP1")

    with col3:
        ganho_brut = float(df_agrupado[df_agrupado.index == subsetor_escolhido]['GANHO BRUTO R$'].values)
        maior_ganho_brut = st.metric(label=f"Ganho Bruto R$ |  TOP {int(ganho_bruto.rank(ascending=False)[subsetor_escolhido])}", 
                    value=f"{ganho_brut :.2f} R$", 
                    delta=f"{(-ganho_bruto.max()) + (ganho_brut):.2f} R$ relativo ao TOP1")


    with col4:
        sr = float(df_agrupado[df_agrupado.index == subsetor_escolhido]['SHARPE'].values)
        maior_sharp_r = st.metric(label=f"Sharpe |  TOP {int(sharpe.rank(ascending=False)[subsetor_escolhido])}", 
                    value=f"{sr :.3f}", 
                    delta=f"{(-sharpe.max() ) + (sr ):.3f} relativo ao TOP1")

    with col7:
        dd = float(df_agrupado[df_agrupado.index == subsetor_escolhido]['MÁXIMO DROW DOWN'].values)
        
        maior_dd = st.metric(label=f"Drow down |  TOP {int(max_dd.rank(ascending=False)[subsetor_escolhido])}", 
                    value=f"{dd * 100:.3f} %", 
                    delta=f"{(-max_dd.max() * 100 ) + (dd * 100):.3f} % relativo ao TOP1")

    with col6:
        dd_bruto = float(df_agrupado[df_agrupado.index == subsetor_escolhido]['MÁXIMO DROW DOWN bruto'].values)
        dd_bruto
        
        maior_dd_bruto = st.metric(label=f"Perda máxima possivel|  TOP {int(max_dd_bruto.rank(ascending=False)[subsetor_escolhido])}", 
                    value=f"{dd_bruto :.3f} R$", 
                    delta=f"{(+max_dd_bruto.max() ) - (dd_bruto ):.3f} R$ relativo ao TOP1")

    with col5:
        medi = float(df_agrupado[df_agrupado.index == subsetor_escolhido]['MÉDIA'].values)
        maior_media = st.metric(label=f"Média do preço da ação |  TOP {int(media.rank(ascending=True)[subsetor_escolhido])}", 
                    value=f"{medi :.2f} R$", 
                    delta=f"{(-media.max()) + (medi):.2f} R$ relativo ao TOP1")
        
except:
    pass

st.divider()
# st.subheader(f'Estatísticas totais das {len(df.groupby("SETOR ECONÔMICO").PAPEL.unique())} ações ( {setor_escolhido} )')
with st.expander('Insights do preço das ações'):
    col1, col2 = st.columns(2)
    with col1:
        maior_rentabilidade = st.metric(label=f" VARIAÇÃO(%) NO PREÇO DO SUBSETOR TOTAL EM 6 MESES", 
                    value=f"{(df.groupby(['SUBSETOR','DATA'])['PREÇO (R$)'].sum()[subsetor_escolhido].iloc[-1] / df.groupby(['SUBSETOR','DATA'])['PREÇO (R$)'].sum()[subsetor_escolhido].iloc[0] - 1) * 100:.3f} %", 
                    delta=f"")

        st.metric(label=f" PREÇO INICIAL MÉDIO DAS AÇÕES DO SUBSETOR NO PERÍODO", 
                    value=f"{(df.groupby(['SUBSETOR','DATA'])['PREÇO (R$)'].sum()[subsetor_escolhido].iloc[0] ):.2F} R$", 
                    delta=f"")
    with col2:
        maior_rentabilidade = st.metric(label=f" VARIAÇÃO(R$) NO PREÇO DO SUBSETOR 6 MESES", 
                    value=f"{(df.groupby(['SUBSETOR','DATA'])['PREÇO (R$)'].sum()[subsetor_escolhido].iloc[-1] - df.groupby(['SUBSETOR','DATA'])['PREÇO (R$)'].sum()[subsetor_escolhido].iloc[0]) :.2f} R$", 
                    delta=f"")
        
        st.metric(label=f" PREÇO INICIAL MÉDIO DAS AÇÕES DO SUBSETOR NO PERÍODO", 
                    value=f"{(df.groupby(['SUBSETOR','DATA'])['PREÇO (R$)'].sum()[subsetor_escolhido].iloc[-1] ):.2F} R$", 
                    delta=f"")

st.divider()
st.subheader('DATAFRAMES', divider='rainbow')

visualizar_tabela = st.toggle('Vizualizar tabelas')
if visualizar_tabela:
    information = st.selectbox(
    'Informações disponíveis', ['Tabela completa', 'Por Subsetor', 'Por informação'])

    if information == 'Tabela completa':
        st.dataframe(df_agrupado)

    if information == 'Por Subsetor':
        subsetor = st.multiselect(
        'SUBSETOR', list(df_agrupado.index.values))
        st.dataframe(df_agrupado.loc[df_agrupado.index.isin(subsetor)])
        pass
    if information == 'Por informação':
        inform = st.multiselect(
        'INFORMAÇÃO', list(df_agrupado.columns))
        st.dataframe(df_agrupado.loc[: , inform])
        # st.table(pd.DataFrame(df_agrupado[[information]]).pivot_table(values='MÉDIA', columns='SUBSETOR'))
        pass
st.divider()
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


######################################################################################################################################################
st.header('RENTABILIDADE ACUMULADA MÊS A MÊS POR SUBSETOR',divider='rainbow')
st.subheader(f"RENTABILIDADE MÉDIA GERAL =  {df['RENTABILIDADE'].mean() * 100:.4f} %")
st.caption('''''')
with st.expander('Insights'):
    st.caption('''Desempenho Relativo dos subsetores: Identificar os subsetores que apresentaram melhor desempenho ao longo dos meses.
    Observar se há algum padrão consistente de liderança ou queda entre os subsetores.''')
    st.caption('''Tendências de Longo Prazo: Identificar tendências de longo prazo em subsetores específicos.
    Avaliar se alguns subsetores são mais propensos a desempenho consistente ao longo do tempo.''')
    st.caption('''Resiliência e Volatilidade: subsetores com rentabilidade acumulada mais estável podem indicar maior resiliência durante diferentes condições de mercado.
    Subsetores mais voláteis podem indicar maior sensibilidade a mudanças econômicas ou eventos específicos.''')
df_perform_setores = df.groupby(['SUBSETOR','DATA'])['ACUM_RENTABILIDADE'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SUBSETOR').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]
if st.checkbox('ver o gráfico'):
    figura = go.Figure()
    

    h_v = st.radio('exibir dataframe da media mensal de rentabilidade acumulada por subsetores',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SUBSETOR')[['ACUM_RENTABILIDADE']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SUBSETOR')[['ACUM_RENTABILIDADE']].mean().T)

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
    figura.update_layout(title='RENTABILIDADE ACUMULADA MÊS A MÊS POR SSUBSETOR')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)





st.divider()
###############################################################################################################################################
st.header('RETORNOS MENSAIS POR SUBSETOR',divider='rainbow')

df_perform_setores = df.groupby(['SUBSETOR','DATA'])['RETORNOS_SIMPLES'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SUBSETOR').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]

figura = go.Figure()
st.subheader(f"MÉDIA DE RETORNO POR MÊS =  {df['RETORNOS_SIMPLES'].mean() * 100:.4f} %")
st.caption('conferir essa media depois ^^^^^^')
with st.expander('Insights'):
    st.caption('''Desempenho Relativo dos subsetores: Compare os retornos mensais entre diferentes setores econômicos. 
            Identifique subsetores que consistentemente superam ou ficam aquém do desempenho geral do mercado. 
            Isso pode indicar áreas de oportunidade ou de risco.''')
    st.caption('''Sazonalidades e Padrões de Desempenho: Observe se existem padrões sazonais nos retornos mensais de determinados setores. 
            Alguns subsetores podem ser mais sensíveis a fatores sazonais, eventos sazonais ou mudanças climáticas.''')
    st.caption('''Correlações com Indicadores Macroeconômicos: Analise se os retornos mensais têm correlação com indicadores econômicos, como taxas de juros, 
            produção industrial, emprego ou outros fatores macroeconômicos. 
            Isso pode ajudar a entender as influências externas nos subsetores.''')
    st.caption('''Identificação de Outliers: Procure por meses em que um subsetor específico teve um desempenho significativamente melhor ou pior do que o esperado. 
            Isso pode indicar eventos específicos que impactaram esse subsetor.''')
    st.caption('''Análise de Consistência: Avalie a consistência dos retornos ao longo do tempo para cada subsetor. 
            subsetores que mantêm um desempenho estável podem ser considerados mais previsíveis.''')
if st.checkbox(' ver   gráfico    '):
    h_v = st.radio('exibir dataframe da média dos retornos mensais por subsetor ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SUBSETOR')[['RETORNOS_SIMPLES']].mean() * 100)
    if h_v == 'HORIZONTAL':
        st.dataframe((df.groupby('SUBSETOR')[['RETORNOS_SIMPLES']].mean() * 100).T)

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
    figura.update_layout(title='Retornos mensais (%) por SUBSETOR')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)





st.divider()
########################################################################################################################################
st.header('ANÁLISE DA VOLATILIDADE MÉDIA POR SUBSETOR',divider='rainbow')
st.subheader(f"VOLATILIDADE MÉDIA GERAL =  {df['VOLATILIDADE'].mean() * 100:.4f} %")
with st.expander('Insights'):
    st.caption('''Comparação de Estabilidade Subsetorial: Ao observar a volatilidade média, você pode identificar setores que 
            historicamente apresentam maior estabilidade e menor flutuação nos preços das ações. 
            Isso pode indicar subsetores mais resilientes a choques externos.''')
    st.caption('''Correlação com Eventos Econômicos: Se houver subsetores que mostram picos de volatilidade em momentos específicos, 
            isso pode estar relacionado a eventos econômicos, políticos ou globais. 
            Analise esses picos para entender as correlações com eventos externos.  OBSERVAR O DROWDOWN/PERGA OU GANHO BRUTO MENSAL PARA MAIS DETALHES''')
st.caption('''''')
df_graf = df.groupby('SUBSETOR')['VOLATILIDADE'].mean() * 100
df_graf = df_graf.sort_values(ascending=False)

if st.checkbox(' ver   gráfico '):

    h_v = st.radio(' exibir tabela VOLATILIDADE média por subsetor   ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SUBSETOR')[['VOLATILIDADE']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SUBSETOR')[['VOLATILIDADE']].mean().T)

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
        title='Volatilidade por subsetores',
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
with st.expander('Insights'):
    st.caption('''Desempenho Relativo dos subsetores: Compare o ganho bruto acumulado entre diferentes subsetores ao longo do tempo.
                Identifique subsetores que apresentam um crescimento mais consistente em termos de ganho bruto.''')
    st.caption('''Análise de Riscos: Avalie a volatilidade nos ganhos brutos acumulados para entender a 
            exposição ao risco em diferentes subsetores.
                Identifique os meses ou períodos de maior volatilidade e investigue as causas.''')
    st.caption('''Eventos Econômicos e Impacto nos subsetores:Relacione eventos econômicos significativos com as 
            mudanças nos ganhos brutos acumulados.
                Analise como eventos como crises econômicas, pandemias ou mudanças nas políticas afetam diferentes subsetores.''')
    st.caption('''Identificação de Tendências: Observe se há tendências crescentes, decrescentes ou estáveis nos ganhos brutos acumulados para cada setor.
    Analise se há padrões sazonais ou eventos específicos que afetam diferentes subsetores.''')
df_perform_setores = df.groupby(['SUBSETOR','DATA'])['ACUM_GANHO BRUTO R$'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SUBSETOR').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]

if st.checkbox(' ver gráfico'):
    figura = go.Figure()


    h_v = st.radio('exibir tabela da média (mensal) de ganho bruto por subsetores  ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SUBSETOR')[['ACUM_GANHO BRUTO R$']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SUBSETOR')[['ACUM_GANHO BRUTO R$']].mean().T)

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
    figura.update_layout(title='Ganho bruto acumulado ao longo dos meses por SUBSETOR')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)

##################################################################################################################################



st.header('ANÁLISE DO DROW DOWN (%) MÉDIO',divider='rainbow')
st.subheader(f"DROW DOWN MÉDIO GERAL =  {df['DROW_DOWN'].mean() * 100:.4f} %")


df_perform_setores = df.groupby(['SUBSETOR','DATA'])['DROW_DOWN'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SUBSETOR').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]
with st.expander('Insights'):
    st.caption('''Resiliência do subsetor: Um Drawdown Médio baixo pode indicar uma resiliência relativamente alta do subsetor, 
               pois os valores negativos médios são menores. Isso sugere que, em média,
                as ações do subsetores têm experimentado quedas menores em comparação com os picos anteriores.''')
    
    st.caption('''Volatilidade: O Drawdown Médio é uma medida da volatilidade do subsetores. 
               Quanto maior o Drawdown Médio, maior a volatilidade. Isso pode influenciar as decisões de investimento, 
               especialmente se você estiver buscando subsetores com menor volatilidade.''')
    st.caption('''Eventos Econômicos: Picos de Drawdown podem estar associados a eventos econômicos significativos, 
               como crises financeiras ou mudanças nas condições do mercado. Analisar os períodos de drawdown 
               pode fornecer insights sobre os eventos que impactaram o subsetor.''')
if st.checkbox('ver gráfico   '):
    figura = go.Figure()

    h_v = st.radio('exibir tabela Drow Down médio mensal por subsetor',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SUBSETOR')[['DROW_DOWN']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SUBSETOR')[['DROW_DOWN']].mean().T)

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
    figura.update_layout(title='Drow down médio mensal por subsetor')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)

####################################################################################################################################

st.header('ANÁLISE DO DROW DOWN MÁXIMO (%)',divider='rainbow')
st.subheader(f"DROW DOWN MÁXIMO MÉDIO =  {df['MÁXIMO DROW DOWN'].mean() * 100:.4f} %")
with st.expander('Insights'):
    st.caption('''Risco Máximo: O Drawdown Máximo fornece uma medida do risco máximo 
            enfrentado por um subsetor em termos de redução do valor. É a maior queda percentual em relação ao pico anterior, 
            representando o risco mais extremo experimentado pelo subsetor durante o período analisado.''')
    st.caption('''Comparação com o Mercado: Comparar o Drawdown Máximo de um subsetor com o do mercado em geral 
            (índices de referência) pode ajudar a determinar se o subsetor é mais ou menos volátil do que o mercado em determinados momentos.''')

if st.checkbox('ver gráfico'):

    h_v = st.radio(' exibir tabela do máximo drow down por subsetor   ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SUBSETOR')[['MÁXIMO DROW DOWN']].mean() * 100)
    if h_v == 'HORIZONTAL':
        st.dataframe((df.groupby('SUBSETOR')[['MÁXIMO DROW DOWN']].mean() * 100).T)

    df_graf = df.groupby('SUBSETOR')['MÁXIMO DROW DOWN'].mean() * 100
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
        title='Drow down máximo por subsetor',
        xaxis_title='Subsetor',
        yaxis_title='DROW DOWN (%)',
        width=1000,
        height=600,
    )
    
    st.plotly_chart(figura)

st.divider()

####################################################################################################################################
st.header('ANÁLISE DA MÉDIA DOS PREÇOS DAS AÇÕES ',divider='rainbow')
st.subheader(f"PREÇO MÉDIO GERAL =  {df['PREÇO (R$)'].mean():.2f} R$")
with st.expander('Insights'):
    st.caption('''Análise subsetorial ou Comparativa: Comparar a média dos preços de um ativo com a média de outros ativos
                do mesmo subsetor ou com índices de referência pode ajudar a contextualizar o desempenho relativo.''')

    st.caption('''Tendência de Longo Prazo: A média dos preços ao longo de períodos mais longos pode ajudar
                a identificar a tendência geral das ações. Uma média móvel de longo prazo suaviza flutuações de curto prazo
                e destaca a direção principal do movimento dos preços.''')
    st.caption('''Análise de Regressão (Opcional):
    Se desejar uma análise mais aprofundada, pode-se realizar uma análise de regressão para entender
                a relação entre a média dos preços e variáveis independentes, 
            como indicadores econômicos ou de desempenho subsetorial.''')


df_perform_setores = df.groupby(['SUBSETOR','DATA'])['PREÇO (R$)'].mean()
todos_setores_econ = df_perform_setores.index.get_level_values('SUBSETOR').unique()
todas_datas = df_perform_setores.index.get_level_values('DATA').unique()
from dateutil.relativedelta import relativedelta
import datetime
data_1_antes = [data - relativedelta(months=1) for data in todas_datas]

if st.checkbox('ver grafico '):
    figura = go.Figure()

    h_v = st.radio('exibir tabela do preço médio mensal das ações  do subsetor    ',['NÃO EXIBIR','HORIZONTAL', 'VERTICAL'], horizontal=True)
    if h_v == 'NÃO EXIBIR':
        pass
    if h_v == 'VERTICAL':
        st.dataframe(df.groupby('SUBSETOR')[['MÉDIA']].mean())
    if h_v == 'HORIZONTAL':
        st.dataframe(df.groupby('SUBSETOR')[['MÉDIA']].mean().T)

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
    figura.update_layout(title='Preço médio mensal das ações por SUBSETOR')
    figura.update_layout(width=1100, height=600)

    st.plotly_chart(figura)


