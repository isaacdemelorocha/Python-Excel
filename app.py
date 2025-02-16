import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar dados de um arquivo Excel
def carregar_dados_excel(uploaded_file):
    """
    Carrega os dados de um arquivo Excel carregado.
    """
    # Ler o arquivo Excel para um DataFrame
    df = pd.read_excel(uploaded_file)

    # Garantir que a coluna 'regiao' seja ordenada corretamente
    df['regiao'] = pd.Categorical(df['regiao'],
                                  categories=["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"],
                                  ordered=True)

    return df

# Função para criar o gráfico de pizza de status geral
def grafico_status_geral(df, cores_status):
    status_counts = df['status do curso'].value_counts()
    fig = px.pie(status_counts, values=status_counts, names=status_counts.index,
                 title="Status dos Cursos por Status Geral", hole=0.3,
                 color=status_counts.index, color_discrete_map=cores_status)
    return fig

# Função para criar o gráfico de pizza por região e status
def grafico_status_por_regiao(df, cores_status):
    status_regiao_counts = df.groupby(['regiao', 'status do curso']).size().reset_index(name='Contagem')
    fig = px.pie(status_regiao_counts, values='Contagem', names='status do curso',
                 title="Distribuição de Cursos por Região e Status",
                 color='status do curso', color_discrete_map=cores_status,
                 facet_col="regiao", facet_col_wrap=5)
    return fig

# Função para exibir as tabelas por região
def exibir_tabelas_por_regiao(df):
    for regiao in df['regiao'].cat.categories:
        st.subheader(f"Tabela - Região {regiao}")
        df_regiao = df[df['regiao'] == regiao]
        st.dataframe(df_regiao)

# Função para criar o gráfico de barras de visão comparativa por região e status
def grafico_visao_comparativa_por_regiao(df, cores_status):
    ranking = df.groupby(['regiao', 'status do curso']).size().reset_index(name='Quantidade')
    ranking['status do curso'] = pd.Categorical(ranking['status do curso'],
                                                categories=['Concluído', 'Em andamento', 'Não iniciado'],
                                                ordered=True)
    fig = px.bar(ranking, x='regiao', y='Quantidade', color='status do curso', title="Visão Comparativa de Regiões por Status dos Cursos",
                 color_discrete_map=cores_status, barmode='stack')
    return fig

# Função principal para configurar o dashboard
def main():
    st.title("Análise de Status de Cursos")

    # Solicitar que o usuário faça o upload de um arquivo Excel
    uploaded_file = st.file_uploader("Carregue um arquivo Excel", type=["xlsx"])

    if uploaded_file is not None:
        # Carregar dados do arquivo Excel
        df = carregar_dados_excel(uploaded_file)

        # Definir cores para o status dos cursos
        cores_status = {
            'Concluído': 'green',
            'Em andamento': 'yellow',
            'Não iniciado': 'red'
        }

        # Exibir gráficos
        st.plotly_chart(grafico_status_geral(df, cores_status))
        st.plotly_chart(grafico_status_por_regiao(df, cores_status))
        st.plotly_chart(grafico_visao_comparativa_por_regiao(df, cores_status))

        # Exibir tabelas separadas por região
        exibir_tabelas_por_regiao(df)

    else:
        st.info("Por favor, faça o upload de um arquivo Excel.")

# Chamar a função principal para executar o dashboard
if __name__ == "__main__":
    main()
