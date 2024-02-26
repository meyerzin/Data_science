import pandas as pd
import streamlit as st
from plotly import graph_objects as go
import time
import numpy as np
import plotly.express as px

df = pd.read_excel('df_completo2.xlsx')


colunas_pct = ['VOLATILIDADE', 'MÁXIMO DROW DOWN', 'RENTABILIDADE']
df_macro = df[['DATA','PAPEL','PREÇO (R$)','IPCA', 'SELIC', 'USD']]
df_macro['RETORNO_DOLAR'] = df_macro['USD'].pct_change()
df_macro.set_index('DATA',inplace=True)

st.title('\t\t:rainbow[UNA INVESTMENT - DATA SCIENCE]')
st.markdown("# Análises MACRO")
st.header('',divider='rainbow')

try:
    colunas_linha1 = st.columns(3)

    col1, col2, col3 = colunas_linha1

# df.loc[df['IPCA'].idxmax(), 'DATA']
    with col1:
        st.subheader('IPCA', divider='gray')
        st.metric(label=f"Maior varição mensal --> {df.loc[df['IPCA'].idxmax(), 'DATA'].strftime('%B - %Y')}", 
                    value=f"{df.IPCA.max() * 100:.2f} %")
        
        st.metric(label=f"Menor varição mensal --> {df.loc[df['IPCA'].idxmin(), 'DATA'].strftime('%B - %Y')}", 
                    value=f"{df.IPCA.min() * 100:.2f} %")
        
        st.metric(label=f"IPCA ACUMULADO 6 MESES", 
                    value=f"{df.IPCA.iloc[0:6].sum()* 100:.2f} %")
        with st.expander('Gráficos'):
            st.caption('variação mensal %')
            st.bar_chart(df_macro['IPCA'].iloc[0:6] * 100)
            st.caption('evolução mensal %')
            st.line_chart(df_macro['IPCA'].iloc[0:6].cumsum() * 100)
        
    with col2:
        st.subheader('SELIC', divider='gray')
        st.metric(label=f"Maior varição mensal --> {df.loc[df['SELIC'].idxmax(), 'DATA'].strftime('%B - %Y')}", 
                    value=f"{df.SELIC.max() * 100:.2f} %")
        
        st.metric(label=f"Menor varição mensal --> {df.loc[df['SELIC'].idxmin(), 'DATA'].strftime('%B - %Y')}", 
                    value=f"{df.SELIC.min() * 100:.2f} %")
        
        st.metric(label=f"SELIC ACUMULADO 6 MESES", 
                    value=f"{df.SELIC.iloc[0:6].sum()* 100:.2f} %")
        with st.expander('Gráficos'):
            st.caption('variação mensal %')
            st.bar_chart(df_macro['SELIC'].iloc[0:6] * 100)
            st.caption('evolução mensal %')
            st.line_chart(df_macro['SELIC'].iloc[0:6].cumsum() * 100)

    with col3:
        st.subheader('DÓLAR', divider='gray')
        st.metric(label=f"Maior preço mensal --> {df.loc[df['USD'].idxmax(), 'DATA'].strftime('%B - %Y')}", 
                    value=f"{df.USD.max() :.2f} R$")
        st.metric(label=f"Menor preço mensal --> {df.loc[df['USD'].idxmin(), 'DATA'].strftime('%B - %Y')}", 
                    value=f"{df.USD.min() :.2f} R$")
        
        st.metric(label=f"Menor varição mensal --> {df.loc[df['USD'].pct_change().idxmin(), 'DATA'].strftime('%B - %Y')}", 
                    value=f"{df.USD.pct_change().min() * 100:.2f} %",
                    delta=f"{(df.set_index('DATA').USD.iloc[0:6] - df.set_index('DATA').USD.iloc[0:6].shift()).min():.2f} R$")
        st.metric(label=f"Maior varição mensal --> {df.loc[df['USD'].pct_change().idxmax(), 'DATA'].strftime('%B - %Y')}", 
            value=f"{df.USD.pct_change().max() * 100:.2f} %",
            delta=f"{(df.set_index('DATA').USD.iloc[0:6] - df.set_index('DATA').USD.iloc[0:6].shift()).max() :.2f} R$")
        
        st.metric(label=f"variação nos 6 meses", 
                    value=f"{(df.USD.iloc[0:6].iloc[-1] / df.USD.iloc[0:6].iloc[0] - 1) * 100:.2f} %",
                    delta=(f'{df.USD.iloc[0:6].iloc[-1] - df.USD.iloc[0:6].iloc[0]:.2f} R$' ))
        with st.expander('Gráficos'):
            st.caption('variação mensal %')
            st.bar_chart(df_macro['RETORNO_DOLAR'].iloc[0:6] * 100)
            st.caption('evolução mensal %')
            st.line_chart(df_macro['USD'].iloc[0:6])
except:
    pass

def destaque_valor_retornos(val):
    if val > 0:
        return 'background-color: green'
    elif val < 0:
        return 'background-color: red'
    else:
        return ''  # Não destaca
st.header('Retorno Mensal das ações nos 6 meses',divider='rainbow')
df_corr = pd.read_excel('df_pivotado_pct_change.xlsx')
st.dataframe(df_corr.set_index('DATA').style.applymap(destaque_valor_retornos))
# df_corr = df_corr.iloc[:, 1:]
df_corr.set_index('DATA',inplace=True)

def destaque_valor_correlacao(val):
    if val == 1:
        return 'background-color: white'
    if abs(val) >= 0.8:
        return 'background-color: green'
    elif abs(val) <= 0.2:
        return 'background-color: red'
    else:
        return ''  # Não destaca




exibir_matriz_corr_inteira = st.toggle('EXIBIR MATRIZ DE CORRELAÇÃO COMPLETA (ordenar por correlação maior individual)')
if exibir_matriz_corr_inteira:
    st.subheader('Matriz de correlação entre todas as ações + dolar, ipca e selic')
    st.caption('Clique na ação para ordenam em ações que mais correlacionam com ela ou menos correlacionam.')
    st.caption('Clique no canto para voltar a disposição normal')
    st.dataframe(df_corr.corr().style.applymap(destaque_valor_correlacao))
st.divider()

st.subheader('Correlações entre TODAS AS AÇÕES (ordenar por rank de todas ações)', divider='rainbow')

corr_matrix = df_corr.corr()

# Transformar a matriz de correlação para longo formato
corr_unstack = corr_matrix.unstack()

# Resetar o índice para transformar em um DataFrame com colunas separadas
corr_df = corr_unstack.reset_index()

# Renomear colunas para melhor entendimento
corr_df.columns = ['Variable1', 'Variable2', 'Correlation']

# Remover correlações perfeitas (variáveis iguais) e duplicatas
corr_df_filtered = corr_df[(corr_df['Variable1'] != corr_df['Variable2']) & (corr_df['Correlation'] < 1)]

# Ordenar pelo valor absoluto da correlação para obter as correlações mais fortes independentemente do sinal
corr_df_filtered['AbsCorrelation'] = corr_df_filtered['Correlation'].abs()

top_corr = corr_df_filtered.sort_values(by='AbsCorrelation', ascending=False)

top_15_corr = top_corr.head(15)

if st.checkbox('Mostrar RANK de correlação'):
    values = st.slider(
    'SELECIONAR RANK DE CORRELAÇÃO DAS AÇÕES',
    1, len(top_corr) + 1, (1, 100))
    st.write('Values:', values)
    
    st.text(f'verificando as correlações de {values}')
    st.dataframe(top_corr.iloc[values[0]:values[1]])
st.divider()
st.header('Correlação IPCA/SELIC/DOLAR --> ações individuais', divider='rainbow')

if st.toggle('Ver infos'):
    st.subheader('Selecione a qtde de dados a ver na tabela a baixo')

    top_ou_tudo = st.radio(
        "Ver:",
        ["Todas", "Melhores 15"],
        index=None,
    )
    if not top_ou_tudo:
        top_ou_tudo = 'TOP 15'

    st.write("Selecionado:", top_ou_tudo)
    st.divider()

    if top_ou_tudo == 'Melhores 15':
        col1,coldiv1,col2,coldiv2,col3 = st.columns([0.7,0.1,0.7, 0.1, 0.7])

        with col1:
            st.subheader('IPCA', divider='rainbow')
            top15_ipca = corr_matrix['IPCA'].drop('IPCA').sort_values(key=abs, ascending=False).head(15)
            st.table(top15_ipca)
        with col2:
            st.subheader('DOLAR', divider='rainbow')
            top15_usd = corr_matrix['USD'].drop('USD').sort_values(key=abs, ascending=False).head(15)
            st.table(top15_usd)
        with col3:
            st.subheader('SELIC', divider='rainbow')
            # Correlações com a SELIC
            top15_selic = corr_matrix['SELIC'].drop('SELIC').sort_values(key=abs, ascending=False).head(15)
            st.table(top15_selic)

    if top_ou_tudo == 'Todas':
        col1,coldiv1,col2,coldiv2,col3 = st.columns([0.7,0.1,0.7, 0.1, 0.7])

        with col1:
            st.subheader('IPCA', divider='rainbow')
            top15_ipca = corr_matrix['IPCA'].drop('IPCA').sort_values(key=abs, ascending=False)
            st.dataframe(top15_ipca,width=300)
        with col2:
            st.subheader('DOLAR', divider='rainbow')
            top15_usd = corr_matrix['USD'].drop('USD').sort_values(key=abs, ascending=False)
            st.dataframe(top15_usd,width=300)
        with col3:
            st.subheader('SELIC', divider='rainbow')
            # Correlações com a SELIC
            top15_selic = corr_matrix['SELIC'].drop('SELIC').sort_values(key=abs, ascending=False)
            st.dataframe(top15_selic,width=300)

    st.divider()

st.header('Correlação IPCA/SELIC/DOLAR --> setor, subsetor e segmento',divider='rainbow')
st.caption('DESENVOLVENDO AINDA, PRONTO FUTURAMENTE')
##################################################################################################################
df_acoes_apenas = df_corr.loc[: , :'YDUQ3']
df_macro_apenas = df_corr[['USD','SELIC','IPCA']]
df_usd = df_macro_apenas.USD
df_ipca = df_macro_apenas.IPCA
df_selic = df_macro_apenas.SELIC



df_correlacoes_3_juntas = pd.DataFrame({'CORR_IPCA' : df_acoes_apenas.corrwith(df_ipca),
                                        'CORR_SELIC' : df_acoes_apenas.corrwith(df_selic),
                                        'CORR_USD' : df_acoes_apenas.corrwith(df_usd)
})

aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SETOR ECONÔMICO','SUBSETOR','SEGMENTO','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()

tab1, tab2, tab3 = st.tabs(["Setor econômico", "Subsetor", "Segmento"])
if st.toggle('Ver tabelas'):
    with tab1:
        st.header('SETOR ECONÔMICO')
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader('CORRELAÇÃO COM IPCA')
            aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SETOR ECONÔMICO','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
            st.dataframe(aham.reset_index().groupby('SETOR ECONÔMICO').CORR_IPCA.mean())
        with col2:
            st.subheader('CORRELAÇÃO COM SELIC')
            aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SETOR ECONÔMICO','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
            st.dataframe(aham.reset_index().groupby('SETOR ECONÔMICO').CORR_SELIC.mean())
        with col3:
            st.subheader('CORRELAÇÃO COM DÓLAR')
            aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SETOR ECONÔMICO','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
            st.dataframe(aham.reset_index().groupby('SETOR ECONÔMICO').CORR_USD.mean())



        with tab2:
            st.header('SUBSETOR')
            col1,col2,col3 = st.columns(3)
            with col1:
                st.subheader('CORRELAÇÃO COM IPCA')
                aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SUBSETOR','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
                st.dataframe(aham.reset_index().groupby('SUBSETOR').CORR_IPCA.mean())
            with col2:
                st.subheader('CORRELAÇÃO COM SELIC')
                aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SUBSETOR','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
                st.dataframe(aham.reset_index().groupby('SUBSETOR').CORR_SELIC.mean())
            with col3:
                st.subheader('CORRELAÇÃO COM DÓLAR')
                aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SUBSETOR','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
                st.dataframe(aham.reset_index().groupby('SUBSETOR').CORR_USD.mean())




        with tab3:
            st.header('SEGMENTO')
            col1,col2,col3 = st.columns(3)
            with col1:
                st.subheader('CORRELAÇÃO COM IPCA')
                aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SEGMENTO','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
                st.dataframe(aham.reset_index().groupby('SEGMENTO').CORR_IPCA.mean())
            with col2:
                st.subheader('CORRELAÇÃO COM SELIC')
                aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SEGMENTO','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
                st.dataframe(aham.reset_index().groupby('SEGMENTO').CORR_SELIC.mean())
            with col3:
                st.subheader('CORRELAÇÃO COM DÓLAR')
                aham = pd.merge(df, df_correlacoes_3_juntas,right_index=True, left_on='PAPEL').groupby(['SEGMENTO','PAPEL'])[['CORR_IPCA','CORR_SELIC','CORR_USD']].mean()
                st.dataframe(aham.reset_index().groupby('SEGMENTO').CORR_USD.mean())
##################################################################################################################
# if st.toggle('Ver infoss'):
#     df.set_index('DATA',inplace=True)
#     df['ret USD'] = df['USD'].pct_change()
#     columns_of_interest = ['SETOR ECONÔMICO','USD', 'IPCA', 'SELIC']

#     # Agrupa por setor econômico e calcule a correlação
#     correlation_by_sector = df[columns_of_interest].groupby('SETOR ECONÔMICO').corr()
#     correlation_by_sector
#     # Exibe a tabela de correlação por setor econômico
#     st.dataframe(correlation_by_sector[correlation_by_sector.index == 'Bens Industriais'])



st.divider()
st.subheader(' QTDE de ações em cada setor, subsetor e segmento ')
st.caption('[possivel jeito de verificar correlação maior de alguns setores do que outros (enquanto nao faço a correlação de fato)]')
top_ipca = corr_matrix['IPCA'].drop('IPCA').sort_values(key=abs, ascending=False)
top_usd = corr_matrix['USD'].drop('USD').sort_values(key=abs, ascending=False)
top_selic = corr_matrix['SELIC'].drop('SELIC').sort_values(key=abs, ascending=False)

if st.checkbox('ver participação da qtde X de ações selecionadas nos grupos'):
    top_selic['TICKER'] = top_selic.index.values

    choice = st.multiselect('escolha um grupo para ver', ['SETOR ECONÔMICO','SUBSETOR','SEGMENTO'])
#################################
    qtde_a_ver = st.radio(
    "quantidade de ações para filtrar",
    [i for i in range(1,len(top_usd))],horizontal=True,
    index=None,)
    st.divider()
#############################
    if  'SETOR ECONÔMICO' in choice:

        st.header('SETOR ECONÔMICO')#,divider='rainbow')
        st.caption('QUANTIDADE DE AÇÕES QUE APARECEM EM CADA SETOR ECONÔMICO, ordenadas por nivel de correlação')
        st.caption('Ações que obtiveram as maiores correlações, ou seja, TOP 10 = as 10 acoes de maior correlação estão em quais setores/subsetores e segmentos?')
        no_dup = df.drop_duplicates(subset='PAPEL')
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader('SELIC', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_selic.head(qtde_a_ver).index.values))]['SETOR ECONÔMICO'].value_counts(dropna=False))

        with c2:
            st.subheader('IPCA', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_ipca.head(qtde_a_ver).index.values))]['SETOR ECONÔMICO'].value_counts(dropna=False))

        with c3:
            st.subheader('DOLAR', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_usd.head(qtde_a_ver).index.values))]['SETOR ECONÔMICO'].value_counts(dropna=False))
        st.divider()

    if 'SUBSETOR' in choice:

        st.header('SUBSETOR')#,divider='rainbow')
        st.caption('QUANTIDADE DE AÇÕES QUE APARECEM EM CADA SUBSETOR')
        no_dup = df.drop_duplicates(subset='PAPEL')
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader('SELIC', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_selic.head(qtde_a_ver).index.values))]['SUBSETOR'].value_counts(dropna=False))

        with c2:
            st.subheader('IPCA', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_ipca.head(qtde_a_ver).index.values))]['SUBSETOR'].value_counts(dropna=False))

        with c3:
            st.subheader('DOLAR', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_usd.head(qtde_a_ver).index.values))]['SUBSETOR'].value_counts(dropna=False))
        st.divider()

    if 'SEGMENTO' in choice:

        st.header('SEGMENTO')#,divider='rainbow')
        st.caption('QUANTIDADE DE AÇÕES QUE APARECEM EM CADA SEGMENTO')
        no_dup = df.drop_duplicates(subset='PAPEL')
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader('SELIC', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_selic.head(qtde_a_ver).index.values))]['SEGMENTO'].value_counts(dropna=False))

        with c2:
            st.subheader('IPCA', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_ipca.head(qtde_a_ver).index.values))]['SEGMENTO'].value_counts(dropna=False))

        with c3:
            st.subheader('DOLAR', divider=True)
            st.table(no_dup[no_dup['PAPEL'].isin(list(top_usd.head(qtde_a_ver).index.values))]['SEGMENTO'].value_counts(dropna=False))
        
        st.divider()



# # Supondo que `df` seja o DataFrame com as informações de setores, subsetores e segmentos
# # e `top10_selic`, `top10_ipca`, `top10_usd` sejam os DataFrames do top 10 correlacionados com SELIC, IPCA e USD

# # Adicione uma coluna 'TICKER' no top10_selic, top10_ipca e top10_usd
# # correspondente ao ticker de cada ação
# top10_selic = pd.merge(top10_selic, df[['TICKER', 'SETOR ECONÔMICO', 'SUBSETOR', 'SEGMENTO']], how='left', left_on='PAPEL', right_on='TICKER')
# top10_ipca = pd.merge(top10_ipca, df[['TICKER', 'SETOR ECONÔMICO', 'SUBSETOR', 'SEGMENTO']], how='left', left_on='PAPEL', right_on='TICKER')
# top10_usd = pd.merge(top10_usd, df[['TICKER', 'SETOR ECONÔMICO', 'SUBSETOR', 'SEGMENTO']], how='left', left_on='PAPEL', right_on='TICKER')

# # Agora você pode usar as funções value_counts() para contar a distribuição nos setores, subsetores e segmentos
# # para cada um dos DataFrames top10
# distribuicao_setor_selic = top10_selic['SETOR ECONÔMICO'].value_counts().reset_index()
# distribuicao_setor_selic.columns = ['SETOR ECONÔMICO', 'Quantidade']

# distribuicao_subsetor_selic = top10_selic['SUBSETOR'].value_counts().reset_index()
# distribuicao_subsetor_selic.columns = ['SUBSETOR', 'Quantidade']

# distribuicao_segmento_selic = top10_selic['SEGMENTO'].value_counts().reset_index()
# distribuicao_segmento_selic.columns = ['SEGMENTO', 'Quantidade']

# # Faça o mesmo para os outros DataFrames (top10_ipca e top10_usd)

# # Exibindo as distribuições
# st.subheader("Distribuição no Top 10 correlacionado com SELIC")
# st.table(distribuicao_setor_selic)
# st.table(distribuicao_subsetor_selic)
# st.table(distribuicao_segmento_selic)

# # Repita o processo para os outros DataFrames (top10_ipca e top10_usd)
        