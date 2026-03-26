# Import das bibliotecas necessarias
import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Configuração da página 
st.set_page_config(
    page_title="Monitor de Preços de Jogos e Consoles", 
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed")

# Barra lateral
with st.sidebar:
    st.header("📌 Sobre o Projeto")
    st.info(
        """
        Este é um **Monitor de Preços Automático** para Jogos e Hardware.
        O sistema extrai os dados diariamente de forma autónoma na nuvem 
        e guarda o histórico para te ajudar a comprar pelo melhor preço!
        """
    )
    st.markdown("---")

    st.subheader("👨‍💻 Desenvolvedor")
    st.markdown("• [Ricardo Vieira Viana](https://www.linkedin.com/in/ricardvviana)")
        
    st.markdown("---")
    
    st.subheader("📂 Código Fonte")
    st.markdown("Acede ao repositório completo e descobre como foi feito:")
    st.link_button("🔗 Ver no GitHub", "https://github.com/RicardViana/automacao-precos-xbox")

# Titulo da página
st.title("🎮 Monitor de Preços: Jogos & Hardware")

# Fonte de dados usada para gerar o dash
FICHEIRO_CSV = "dados/historico_precos.csv"

# ==============================================================================
# FUNÇÃO PARA GERAR O GRÁFICO E TABELA (Usada nas Abas)
# ==============================================================================
def exibir_dashboard_produto(df_categoria, chave_selectbox):
    """Gera a interface (Selectbox, Métricas, Gráficos e Tabela) para a categoria escolhida."""
    
    if df_categoria.empty:
        st.warning("Ainda não há dados suficientes para esta categoria.")
        return

    # 1. Criar uma lista com os nomes únicos guardados no CSV
    lista_de_itens = df_categoria['Nome'].unique()
    
    # 2. Criar uma caixa de seleção para escolher o produto
    item_selecionado = st.selectbox("Escolhe um item para analisar:", lista_de_itens, key=chave_selectbox)
    
    # 3. Filtrar os dados do item selecionado e ordenar cronologicamente
    df_filtrado = df_categoria[df_categoria['Nome'] == item_selecionado].sort_values(by="Data")
    
    if not df_filtrado.empty:
        link_item = df_filtrado['Link'].iloc[0]
        st.markdown(f"**Link:** [Acessar Loja]({link_item})")
        st.markdown("---")

        # Calcular métricas para o Dashboard
        preco_atual = df_filtrado['Preco'].iloc[-1]
        
        # Mais de um dia de histórico calcular a diferença para mostrar
        se_houver_historico = len(df_filtrado) > 1
        preco_anterior = df_filtrado['Preco'].iloc[-2] if se_houver_historico else preco_atual
        diferenca = preco_atual - preco_anterior
        
        # Mostrar Delta se houver uma variação real no preço
        if se_houver_historico and diferenca != 0:
            delta_formatado = f"R$ {diferenca:.2f}"
        else:
            delta_formatado = None
        
        # Mostrar o preço com uma setinha verde/vermelha dependendo se subiu ou desceu
        st.metric(label="Preço Mais Recente", 
                  value=f"R$ {preco_atual:.2f}", 
                  delta=delta_formatado,
                  delta_color="inverse")
        
        st.markdown("---")

        # Criar o gráfico com Plotly
        st.write("### Evolução do Preço ao Longo do Tempo")
        
        df_grafico = df_filtrado.copy()
        df_grafico['Data_Exibicao'] = df_grafico['Data'].dt.strftime('%d/%m/%Y')
        
        # Configuração do grafico (Eixo X volta a ser apenas a Data)
        fig = px.line(
            df_grafico, 
            x='Data', 
            y='Preco', 
            markers=True,
            hover_data={"Data": False, "Data_Exibicao": True, "Hora": True},
            labels={'Data': 'Data', 'Preco': 'Preço (R$)', 'Data_Exibicao': 'Data', 'Hora': 'Atualizado às'}
        )
        
        # Força o eixo Y, formata eixo X e reduz a altura total
        fig.update_layout(
            yaxis=dict(autorange=True),
            xaxis=dict(tickformat="%d/%m/%Y"), # Garante que o eixo X mostra apenas Dia/Mês/Ano
            margin=dict(t=0, b=30, l=0, r=0),
            height=300,
            xaxis_title="Linha do Tempo",
            hovermode="x unified"
        )
        
        # Mostra o gráfico no Streamlit
        st.plotly_chart(fig, width='stretch')
        
        # Tabela de dados apenas do jogo selecionado
        st.write("### Histórico de Registos")
        
        # Filtrar as colunas e ordenar da mais recente para a mais antiga
        tabela_exibicao = df_filtrado[['Data', 'Hora', 'Preco']].sort_values(by="Data", ascending=False)
        
        # Formatar a coluna 'Data' para mostrar apenas Ano-Mês-Dia
        tabela_exibicao['Data'] = tabela_exibicao['Data'].dt.strftime('%Y-%m-%d')
        
        # Exibir a tabela ocultando o índice
        st.dataframe(tabela_exibicao, hide_index=True, width='stretch')

# ==============================================================================
# CARREGAMENTO DOS DADOS E SEPARAÇÃO DE ABAS
# ==============================================================================
if os.path.exists(FICHEIRO_CSV):
    df = pd.read_csv(FICHEIRO_CSV)
    
    # 1. TRATAMENTO DA HORA: Se a coluna Hora não existir, cria-a
    if 'Hora' not in df.columns:
        df['Hora'] = "-"
    
    # Substituir os valores vazios das linhas antigas por um traço "-"
    df['Hora'] = df['Hora'].fillna("-").replace("", "-")
    
    # 2. TRATAMENTO DA DATA
    df['Data'] = pd.to_datetime(df['Data']) 

    # 3. SEPARAÇÃO DAS LOJAS (Usando a nova coluna 'Loja' do CSV)
    # Se a coluna Loja não existir no CSV antigo, assumimos que é tudo Xbox
    if 'Loja' not in df.columns:
        df['Loja'] = 'xbox'
        
    df_jogos = df[df['Loja'] == 'xbox']
    df_consoles = df[df['Loja'] == 'mercadolivre']

    # 4. CRIAR AS ABAS NA TELA
    aba_jogos, aba_consoles = st.tabs(["🕹️ Jogos Digitais (Xbox)", "🎮 Consoles & Hardware"])

    # Preencher Aba 1 (Jogos)
    with aba_jogos:
        exibir_dashboard_produto(df_jogos, chave_selectbox="sb_jogos")

    # Preencher Aba 2 (Consoles)
    with aba_consoles:
        exibir_dashboard_produto(df_consoles, chave_selectbox="sb_consoles")

else:
    st.info("Ainda não existem dados no ficheiro CSV. O script de automação precisa rodar primeiro!")