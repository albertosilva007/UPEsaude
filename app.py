import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dadossaude.csv', skiprows=1)
    df.columns = [f'Coluna{i+1}' for i in range(df.shape[1])]  # Nomeia as colunas corretamente
    return df

df = carregar_dados()

# Título
st.title("📊 Análise de Indicadores de Saúde")

# Introdução
st.markdown("""
Este projeto visa analisar um conjunto de indicadores de saúde, buscando identificar padrões, e sugerir melhorias para a gestão pública.
""")

st.header("🎯 Filtros de Dados")

# --- NOVO: Adicionar Filtros
col1, col2 = st.columns(2)

with col1:
    coluna_filtro = st.selectbox('Deseja filtrar por qual coluna?', df.columns)
with col2:
    if df[coluna_filtro].dtype in ['int64', 'float64']:
        valor_min, valor_max = st.slider(
            f'Selecione o intervalo para {coluna_filtro}:',
            float(df[coluna_filtro].min()), 
            float(df[coluna_filtro].max()), 
            (float(df[coluna_filtro].min()), float(df[coluna_filtro].max()))
        )
        df = df[(df[coluna_filtro] >= valor_min) & (df[coluna_filtro] <= valor_max)]
    else:
        categorias = df[coluna_filtro].dropna().unique()
        selecao = st.multiselect(f'Selecione os valores para {coluna_filtro}:', categorias, default=list(categorias))
        df = df[df[coluna_filtro].isin(selecao)]

# Gráfico 1 - Distribuição de uma coluna
st.header("📈 Visualizações dos Indicadores")
coluna_escolhida = st.selectbox('Escolha uma coluna para visualizar a distribuição:', df.columns)
fig1 = px.histogram(df, x=coluna_escolhida, nbins=30, title=f'Distribuição de {coluna_escolhida}')
fig1.update_layout(bargap=0.1)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2 - Comparativo entre duas colunas
st.subheader("📊 Comparativo entre Indicadores")
coluna_x = st.selectbox('Coluna para eixo X', df.columns, index=0, key='x')
coluna_y = st.selectbox('Coluna para eixo Y', df.columns, index=1, key='y')

if coluna_x != coluna_y:
    fig2 = px.scatter(
        df, 
        x=coluna_x, 
        y=coluna_y, 
        title=f'Relação entre {coluna_x} e {coluna_y}',
        opacity=0.7,
        color_discrete_sequence=['#636EFA']  # cor azul legal
    )
    fig2.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Por favor, selecione colunas diferentes para o comparativo.")

# Estatísticas descritivas
st.header("📋 Resumo Estatístico")
st.dataframe(df.describe())

# Conclusão
st.header("💡 Conclusões e Possíveis Soluções")
st.markdown("""
- 🔍 **Identificação de Indicadores Críticos**: Colunas com altos desvios ou médias elevadas podem indicar áreas problemáticas.
- 📊 **Correlações Relevantes**: Indicadores fortemente correlacionados sugerem onde intervir primeiro.
- 🌍 **Próximos passos**: Investigar os locais/regiões associadas às piores performances para políticas de saúde mais eficazes.

✨ Esta análise é apenas o começo! Novas fontes e integrações podem gerar insights ainda mais profundos.
""")

st.caption("Projeto desenvolvido para o Desafio de Visualização de Dados com Streamlit - 2025")
