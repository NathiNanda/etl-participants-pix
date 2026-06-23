import streamlit as st
import sqlite3
import pandas as pd
import os
import altair as alt

st.set_page_config(page_title='Participantes do PIX', layout="wide")

@st.cache_data()
def load_data():
    # Path to the database
    db_path = os.path.join("data", "processed", "pix.db")
    # Connect to the database
    connection = sqlite3.connect(db_path)
    # Load the data directly into a Pandas DataFrame
    query = "SELECT * FROM participantes_pix;"
    df = pd.read_sql_query(query, connection)
    # Close the connection
    connection.close()
    return df

df = load_data()

# ==================== SIDEBAR (FILTERS) ===================== #
st.sidebar.header("Filtros")

# Dropdown for participation modality
add_selectbox_modalidade = st.sidebar.selectbox(
    'Modalidade de Participação',
    df['modalidade_participacao'].unique(),
    index=None,
)

add_selectbox_tipo = st.sidebar.selectbox(
    'Tipo de Participação',
    df['tipo_participacao'].unique(),
    index=None,
)

add_selectbox_categoria = st.sidebar.selectbox(
    'Categoria de Instituição',
    df['categoria_instituicao'].unique(),
    index=None,
)

# ==================== APPLYING FILTERS ===================== #
df_filtrado = df.copy()

if add_selectbox_modalidade is not None:
    df_filtrado = df_filtrado[df_filtrado.modalidade_participacao == add_selectbox_modalidade]
if add_selectbox_tipo is not None:
    df_filtrado = df_filtrado[df_filtrado.tipo_participacao == add_selectbox_tipo]
if add_selectbox_categoria is not None:
    df_filtrado = df_filtrado[df_filtrado.categoria_instituicao == add_selectbox_categoria]

# ==================== MAIN CONTENT ===================== #
st.title("Visualização dos Participantes do PIX")
st.markdown("Análise interativa dos dados de participantes cadastrados no Banco Central obtidos via BrasilAPI.")

# Top Metrics Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Participantes", len(df_filtrado))
with col2:
    diretos = len(df_filtrado[df_filtrado['tipo_participacao'] == 'Direta'])
    st.metric("Participação Direta", diretos)
with col3:
    indiretos = len(df_filtrado[df_filtrado['tipo_participacao'] == 'Indireta'])
    st.metric("Participação Indireta", indiretos)
st.divider()

# Graphics
graf1, graf2 = st.columns(2)

with graf1:
    st.subheader("Participação por Modalidade")
    modalidade_counts = df_filtrado['modalidade_participacao'].value_counts().reset_index()

    chart_mod = alt.Chart(modalidade_counts).mark_bar().encode(
        x=alt.X('modalidade_participacao:N', sort='-y', title='Modalidade'),
        y=alt.Y('count:Q', title='Quantidade')
    )
    st.altair_chart(chart_mod, use_container_width=True)

with graf2:
    st.subheader("Participação por Tipo")
    tipo_counts = df_filtrado['tipo_participacao'].value_counts().reset_index()

    chart_tipo = alt.Chart(tipo_counts).mark_bar().encode(
        x=alt.X('tipo_participacao:N', sort='-y', title='Tipo'),
        y=alt.Y('count:Q', title='Quantidade')
    )
    st.altair_chart(chart_tipo, use_container_width=True)

st.subheader("Categorias de Instituição")
categoria_counts = df_filtrado['categoria_instituicao'].value_counts().reset_index()
chart_cat = alt.Chart(categoria_counts).mark_bar().encode(
        x=alt.X('count:Q', title='Quantidade'),
        y=alt.Y('categoria_instituicao:N', sort='-x', title='Categoria')
)
st.altair_chart(chart_cat, use_container_width=True)
    

# Filtered Table
st.subheader("📋 Tabela de Participantes")
st.dataframe(df_filtrado, use_container_width=True)