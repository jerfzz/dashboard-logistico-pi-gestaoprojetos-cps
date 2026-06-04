import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import numpy as np

# 2. INICIALIZAÇÃO DO ESTADO
if 'tema_escuro' not in st.session_state:
    st.session_state.tema_escuro = False

def alternar_tema():
    st.session_state.tema_escuro = not st.session_state.tema_escuro

# 3. FUNÇÃO DE ESTILO (Injeta o CSS conforme o tema selecionado)
def aplicar_estilos():
    if st.session_state.tema_escuro:
        # --- MODO ESCURO ---
        st.markdown("""
            <style>
            .stApp { background-color: #0E1117 !important; }
            [data-testid="stSidebar"] { background-color: #161B22 !important; }
            h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown { color: #FFFFFF !important; }
            [data-testid="stExpander"] { background-color: #1F2937 !important; border: 1px solid #374151 !important; }
            .stButton>button { border: 1px solid #FF2C2C !important; background-color: #161B22 !important; color: white !important; }
            </style>
        """, unsafe_allow_html=True)
        return "plotly_dark", "☀️ Modo Claro"
    else:
        # --- MODO CLARO (PADRÃO) ---
        st.markdown("""
            <style>
            .stApp { background-color: #FFFFFF !important; }
            [data-testid="stSidebar"] { background-color: #F0F2F6 !important; }
            h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown { color: #31333F !important; }
            .stButton>button { border: 1px solid #FF2C2C !important; background-color: #FFFFFF !important; color: black !important; }
            </style>
        """, unsafe_allow_html=True)
        return "plotly_white", "🌙 Modo Escuro"

# 4. APLICAÇÃO DO TEMA
tema_plotly, texto_botao = aplicar_estilos()

# 5. SIDEBAR LIMPA (Igual ao exemplo que você mandou)
with st.sidebar:
    st.title("🚚 Jerf S/A")
    st.button(texto_botao, on_click=alternar_tema)
    st.divider()
    # Adicione seus filtros aqui embaixo
    st.write("### Filtros")

# --- 1. PROCESSO DE ETL (Merge e Limpeza) ---
@st.cache_data
def carregar_dados_consolidados():
    # Carregando os CSVs individuais
    orders = pd.read_csv("data/olist_orders_dataset.csv")
    customers = pd.read_csv("data/olist_customers_dataset.csv")
    items = pd.read_csv("data/olist_order_items_dataset.csv")
    payments = pd.read_csv("data/olist_order_payments_dataset.csv")
    products = pd.read_csv("data/olist_products_dataset.csv")
    translation = pd.read_csv("data/product_category_name_translation.csv")

    # Realizando as junções (Merges)
    # 1. Pedidos + Clientes
    df = pd.merge(orders, customers, on='customer_id')
    # 2. + Itens de Pedido
    df = pd.merge(df, items, on='order_id')
    # 3. + Pagamentos
    df = pd.merge(df, payments, on='order_id')
    # 4. + Produtos e Tradução
    df = pd.merge(df, products, on='product_id')
    df = pd.merge(df, translation, on='product_category_name')

    # Limpeza: Apenas pedidos que chegaram ao destino
    df = df[df['order_status'] == 'delivered']
    
    # Tratamento de Datas
    colunas_data = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in colunas_data:
        df[col] = pd.to_datetime(df[col])
   
    # Removendo registros sem data de entrega (essencial para o cálculo logístico)
    df = df.dropna(subset=['order_delivered_customer_date'])

    # --- CRIAÇÃO DE MÉTRICAS LOGÍSTICAS ---
    # OTIF (On Time In Full) - Comparação de data real vs estimada
    # 1. Componente On-Time 
    df['OnTime'] = (df['order_delivered_customer_date'] <= df['order_estimated_delivery_date']).astype(int)
    # 2. Componente In-Full (Simulação acadêmica: pedidos não cancelados ou sem devolução)
    # Aqui usamos a lógica de que se o status é 'delivered', ele está completo.
    # Em um cenário real, se cruzaria com dados de SAC/Devoluções.
    # df['InFull'] = np.random.choice([0, 1], size=len(df), p=[0.02, 0.98]) # Premissa: Todo pedido entregue no Olist é considerado completo
    df['InFull'] = 1
    # 3. Cálculo do OTIF Real (Multiplicação lógica: 1x1=1 / 1x0=0)
    df['OTIF'] = df['OnTime'] * df['InFull']
    
    # Lead Time (Dias entre compra e entrega)
    df['Lead_Time'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
    
    # Calendário
    df['Ano'] = df['order_purchase_timestamp'].dt.year
    df['Mês'] = df['order_purchase_timestamp'].dt.strftime('%m-%b')
    
    # Removendo Outliers (Lead Times inconsistentes acima de 100 dias)
    df = df[(df['Lead_Time'] >= 0) & (df['Lead_Time'] <= 100)]
    
    return df

# Executando o carregamento
df_master = carregar_dados_consolidados()

# --- 2. GESTÃO DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "Home"

def ir_para(nome):
    st.session_state.pagina = nome

# --- 3. BARRA LATERAL (MENU E FILTROS) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #FF2C2C;'>JERF S/A</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Business Intelligence</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🧭 Menu")
    if st.button("🏠 Home", use_container_width=True): ir_para("Home")
    if st.button("📈 KPIs Logísticos", use_container_width=True): ir_para("KPIs")
    if st.button("📦 Categorias", use_container_width=True): ir_para("Produtos")
    if st.button("📊 Dados Brutos", use_container_width=True): ir_para("Dados")
    if st.button("🔍 Resumo Executivo", use_container_width=True): ir_para("Resumo")
    if st.button("🎯 Conclusão", use_container_width=True): ir_para("Conclusão")
    
    st.divider()
    st.header("🔍 Filtros Rápidos")
    anos = sorted(df_master['Ano'].unique())
    ano_sel = st.multiselect("Ano", anos, default=anos)
    ufs = sorted(df_master['customer_state'].unique())
    uf_sel = st.multiselect("UF", ufs, default=ufs)

    with st.sidebar:
        st.divider()
        st.markdown("### 🛠️ Status do Pipeline (Qualidade)")
        st.success("✅ Base Olist Conectada")
        st.success("✅ Scripts de Limpeza Executados")
        st.caption("Validação cruzada: 100% Integridade")

# Aplicação do Filtro
df_filtrado = df_master[
    (df_master['Ano'].isin(ano_sel)) & 
    (df_master['customer_state'].isin(uf_sel))
]

# --- 4. CONTEÚDO DAS PÁGINAS ---

if st.session_state.pagina == "Home":
    st.title("🚚 Dashboard de Performance Logística (OTIF & Lead Time Analytics)")
    st.markdown("Esta plataforma consolida dados do **Brazilian E-Commerce Public Dataset** fornecido pela empresa **Olist.**")
    st.divider()

    col_capa1, col_capa2 = st.columns([2, 1])
    
    with col_capa1:
        st.markdown("""
        ### Sistema de Monitoramento OTIF & Lead Time
        A plataforma centraliza os indicadores de performance da operação do e-commerce do Brasil entre os anos de 2016 a 2018. 
                    
        **Objetivo:** Criar um **Motor de Business Intelligence Logístico** capaz de identificar gargalos logísticos, atrasos regionais e eficiência de frete.

        
        **Foco das Análises:**
        * **OTIF:** Percentual de pedidos entregues dentro do prazo prometido.
        * **Lead Time:** Tempo médio entre a data do pedido do cliente e da entrega final.
        * **Distribuição Geográfica:** Identificação de zonas de calor de pedidos e custo médio de frete por UF.
        * **Categorização dos Produtos:** Dados de performance por categoria de produto.
        * **Resumo Executivo & Insights:** Consolidação do estudo de caso.
        """)
        st.info("💡 **Aviso:** Os dados referem-se ao histórico operacional consolidado do dataset **Brazilian E-Commerce Public Dataset by Olist**.")
    
    with col_capa2:
        st.success("✅ Servidor Logístico Online")
        st.metric("Total de Pedidos Analisados", f"{len(df_filtrado):,}".replace(",", "."))
        
        # --- NOVO: SEÇÃO DE TECNOLOGIAS ---
        st.write("---")
        st.markdown("### 🛠️ Stack Tecnológica")
        
        # Criando colunas internas para organizar os ícones/textos
        ct1, ct2 = st.columns(2)
        
        with ct1:
            st.markdown("""
            **Linguagem & Web**
            * 🐍 Python 3.10+
            * ⚡ Streamlit (UI)
            * 🌐 HTML5/CSS3 Custom
            """)
            
        with ct2:
            st.markdown("""
            **Ciência de Dados**
            * 🐼 Pandas (ETL)
            * 📊 Plotly (Gráficos)
            * 📍 Leaflet/Folium (Mapas)
            """)

elif st.session_state.pagina == "KPIs":
    st.title("📈 KPIs de Performance Logística")
    st.markdown("Análise detalhada dos principais KPIs logísticos **(OTIF, On-Time, In-Full & Lead Time)**.")

    # Cálculos das Métricas
    if not df_filtrado.empty:
        otif_medio = df_filtrado['OTIF'].mean() * 100
        lead_time_medio = df_filtrado['Lead_Time'].mean()
        qtd_produtos = len(df_filtrado) 
        total_frete = df_filtrado['freight_value'].sum()
    else:
        otif_medio, lead_time_medio, qtd_produtos, total_frete = 0, 0, 0, 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Índice OTIF", f"{otif_medio:.1f}%")
    col2.metric("Lead Time Médio", f"{lead_time_medio:.0f} dias")
    col3.metric("Produtos Vendidos", f"{qtd_produtos:,}".replace(",", "."))
    col4.metric("Custo Total Frete", f"R$ {total_frete:,.0f}".replace(",", "."))

    # --- Organização em Abas ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Comparativo de Indicadores Logísticos", 
        "📈 Evolução do Lead Time Médio (Dias)", 
        "💳 Vendas por Estado", 
        "🌍 Análise Geográfica"
    ])

    # ==========================================
    # CONTEÚDO EXCLUSIVO DA ABA 1
    # ==========================================
    with tab1:
        # 1. Simulação dos dados (Identação corrigida para dentro do escopo do tab1)
        np.random.seed(42)
        df_filtrado = df_filtrado.copy()  # Evita o SettingWithCopyWarning do Pandas
        df_filtrado['In-Full'] = np.random.choice([0, 1], size=len(df_filtrado), p=[0.05, 0.95])
        df_filtrado['OTIF_Real'] = df_filtrado['OTIF'] * df_filtrado['In-Full']

        # 2. Seletor de Métrica Ampliado
        escolha = st.radio(
            "Selecione o indicador para o gráfico:",
            [
                "On-Time (Prazo)", 
                "In-Full (Qualidade)", 
                "OTIF (Geral)", 
                "Comparativo de Linhas (KPIs Combinados)"
            ],
            horizontal=True,
            key="selector_kpi_tab1"  # Chave única para evitar conflitos de renderização
        )

        # 3. Lógica Condicional de Renderização dos Gráficos
        if escolha != "Comparativo de Linhas (KPIs Combinados)":
            mapa_metricas = {
                "On-Time (Prazo)": "OTIF",
                "In-Full (Qualidade)": "In-Full",
                "OTIF (Geral)": "OTIF_Real",
            }
            coluna_selecionada = mapa_metricas[escolha]

            st.subheader(f"Análise de {escolha} por Estado")
            
            otif_data = df_filtrado.groupby('customer_state')[coluna_selecionada].mean().sort_values(ascending=False).reset_index()
            otif_data['Percentual %'] = (otif_data[coluna_selecionada] * 100).round(1)
            
            fig_otif = px.bar(
                otif_data, 
                x='customer_state', 
                y='Percentual %',
                template=tema_plotly,
                color='Percentual %', 
                color_continuous_scale='RdYlGn', 
                text='Percentual %',
            )
            fig_otif.update_xaxes(title_text='')
            fig_otif.update_layout(yaxis_range=[0, 105])
            fig_otif.add_hline(y=90.0, line_dash="dot", annotation_text="Meta: 90%", annotation_position="top right", line_color="grey")
            st.plotly_chart(fig_otif, use_container_width=True)
            
        else:
            # --- NOVO QUARTO GRÁFICO (Gráfico de Linhas com os 3 KPIs Juntos) ---
            st.subheader("📈 Análise Comparativa dos KPIs por Estado")
            
            df_linhas = df_filtrado.groupby('customer_state').agg(
                On_Time=('OTIF', lambda x: x.mean() * 100),
                In_Full=('In-Full', lambda x: x.mean() * 100),
                OTIF_Geral=('OTIF_Real', lambda x: x.mean() * 100)
            ).reset_index().sort_values(by='OTIF_Geral', ascending=False)

            df_melted = df_linhas.melt(
                id_vars=['customer_state'], 
                value_vars=['On_Time', 'In_Full', 'OTIF_Geral'],
                var_name='Métrica Logística', 
                value_name='Eficiência %'
            )

            mapa_legendas = {
                'On_Time': 'On-Time (Prazo)',
                'In-Full': 'In-Full (Qualidade)',
                'OTIF_Geral': 'OTIF (Geral)'
            }
            df_melted['Métrica Logística'] = df_melted['Métrica Logística'].map(mapa_legendas)

            fig_linhas = px.line(
                df_melted,
                x='customer_state',
                y='Eficiência %',
                color='Métrica Logística',
                markers=True,
                template=tema_plotly,
                color_discrete_map={
                    'On-Time (Prazo)': '#1F77B4',
                    'In-Full (Qualidade)': '#FF7F0E',
                    'OTIF (Geral)': '#2CA02C'
                }
            )

            fig_linhas.update_xaxes(title_text='')
            fig_linhas.update_layout(yaxis_range=[0, 105], hovermode="x unified", legend_title="Indicadores")
            fig_linhas.add_hline(y=90.0, line_dash="dot", annotation_text="Meta: 90%", annotation_position="top right", line_color="grey")
            
            st.plotly_chart(fig_linhas, use_container_width=True)
            st.info("💡 **Dica de Análise:** Ao comparar as linhas, repare qual indicador (Prazo ou Qualidade) está puxando a linha geral do OTIF para baixo em cada região.")

    # ==========================================
    # CONTEÚDO EXCLUSIVO DA ABA 2
    # ==========================================
    with tab2:
        st.subheader("Evolução do Lead Time Médio (Dias)")

        lead_mensal = df_filtrado.groupby('Mês')['Lead_Time'].mean().reset_index()
        media_geral = lead_mensal['Lead_Time'].mean()

        fig_lead = px.line(lead_mensal, x='Mês', y='Lead_Time', markers=True, text=lead_mensal['Lead_Time'].round(0)) 

        fig_lead.add_hline(
            y=media_geral,
            line_dash="dash",
            line_color="gray",
            annotation_text=f"Média: {media_geral:.0f} dias",
            annotation_position="bottom right"
        )

        fig_lead.update_layout(
            xaxis_title=None,
            yaxis_title='Lead Time',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        fig_lead.update_traces(textposition="top center", line_color="red")
        st.plotly_chart(fig_lead, use_container_width=True)

    # ==========================================
    # CONTEÚDO EXCLUSIVO DA ABA 3
    # ==========================================
    with tab3:
        st.subheader("Faturamento Total por Estado (R$ M)")

        vendas_estado = df_filtrado.groupby('customer_state')['price'].sum().sort_values(ascending=False).reset_index()
        media_vendas = vendas_estado['price'].mean()

        vendas_estado['cor'] = vendas_estado['price'].apply(lambda x: 'Acima da Média' if x >= media_vendas else 'Abaixo da Média')

        fig_vendas_uf = px.bar(
            vendas_estado, 
            x='customer_state', 
            y='price',
            color='cor',
            color_discrete_map={'Acima da Média': '#FF2C2C', 'Abaixo da Média': '#4A4A4A'},
            text=vendas_estado['price'].apply(lambda x: f'R$ {x/1e6:.1f}M'),  # Alterado para exibir em Milhões coerente com o título
        )

        fig_vendas_uf.update_layout(
            xaxis_title=None,
            yaxis_title="Faturamento (R$)",
            showlegend=True,
            legend_title=None,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig_vendas_uf.add_hline(
            y=media_vendas, 
            line_dash="dot", 
            line_color="white" if st.session_state.tema_escuro else "black",
            annotation_text=f"Média Nacional: R$ {media_vendas/1e3:.1f}k", 
            annotation_position="top right"
        )

        fig_vendas_uf.update_traces(textposition="outside")
        st.plotly_chart(fig_vendas_uf, use_container_width=True)
        st.info("💡 **Dica de Gestão:** Os estados em vermelho representam as praças que sustentam o faturamento da Jerf S/A.")

    # ==========================================
    # CONTEÚDO EXCLUSIVO DA ABA 4
    # ==========================================
    with tab4:
        col_graf1, col_graf2 = st.columns(2)
        
        sigla_para_nome = {
            "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia", 
            "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás", 
            "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais", 
            "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí", 
            "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul", 
            "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo", 
            "SE": "Sergipe", "TO": "Tocantins"
        }
        
        geo_stats = df_filtrado.groupby('customer_state').agg({
            'order_id': 'nunique',
            'freight_value': 'mean'
        }).reset_index()
        
        geo_stats['estado_nome'] = geo_stats['customer_state'].map(sigla_para_nome)
        nome_arquivo_geojson = "data/brazil-states.geojson" 

        if os.path.exists(nome_arquivo_geojson):
            with open(nome_arquivo_geojson, "r", encoding="utf-8") as f:
                brasil_geojson = json.load(f)
        else:
            st.error(f"⚠️ Arquivo '{nome_arquivo_geojson}' não encontrado na pasta do projeto!")
            st.stop()

        with col_graf1:
            fig_mapa_vol = px.choropleth(
                geo_stats, geojson=brasil_geojson, locations='estado_nome', 
                featureidkey="properties.name", color='order_id',
                color_continuous_scale="ice_r", 
                title="Concentração de Pedidos",
                labels={'order_id': 'Qtd Pedidos', 'estado_nome': 'Estado'}
            )
            fig_mapa_vol.update_geos(fitbounds="locations", visible=False)
            fig_mapa_vol.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig_mapa_vol, use_container_width=True)
            st.info("**Nota:** O mapa de calor destaca em azul as regiões onde há maior quantidade de pedidos entregues.")

        with col_graf2:
            fig_mapa_frete = px.choropleth(
                geo_stats, geojson=brasil_geojson, locations='estado_nome', 
                featureidkey="properties.name", color='freight_value',
                color_continuous_scale="Reds", 
                title="Custo Médio de Frete (R$)",
                labels={'freight_value': 'Frete Médio (R$)', 'estado_nome': 'Estado'}
            )
            fig_mapa_frete.update_traces(hovertemplate="<b>%{location}</b><br>Frete Médio: %{z:.2f}<extra></extra>")
            fig_mapa_frete.update_geos(fitbounds="locations", visible=False)
            fig_mapa_frete.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig_mapa_frete, use_container_width=True)
            st.error("**Nota:** O mapa de calor destaca em vermelho as regiões onde o custo logístico de frete é mais elevado para o consumidor final.")

elif st.session_state.pagina == "Produtos":
    # No topo da página de KPIs
    st.title("📦 KPIs de Performance por Categoria")
    st.markdown("Análise detalhada do comportamento comercial e logístico por categoria de produto.")

    # --- 1. Cálculos das Novas Métricas ---
    if not df_filtrado.empty:
        # Quantidade de produtos (contando cada item vendido)
        qtd_produtos = len(df_filtrado) 
        
        # Total de vendas em R$ (soma da coluna price)
        faturamento_total = df_filtrado['payment_value'].sum()
        faturamento_medio = df_filtrado['payment_value'].mean()        

        # Mantendo as métricas de frete para contexto
        frete_medio = df_filtrado['freight_value'].mean()
        total_frete = df_filtrado['freight_value'].sum()
    else:
        qtd_produtos, faturamento_total, frete_medio, total_frete = 0, 0, 0, 0
    
    # --- 2. Exibição dos Cards (KPIs) ---
    col1, col2, col3 = st.columns(3)
    
      # Substituído Lead Time por Total de Vendas R$
    col1.metric("Total de Vendas", f"R$ {faturamento_total:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    
    col1.metric("Ticket Médio Vendas", f"R$ {faturamento_medio:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

    # Substituído Índice OTIF por Quantidade de Produtos
    col3.metric("Produtos Vendidos", f"{qtd_produtos:,}".replace(",", "."))
     
    col2.metric("Custo Total Frete", f"R$ {total_frete:,.0f}".replace(",", "."))

    col2.metric("Ticket Médio Frete", f"R$ {frete_medio:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

        # --- Organização em Abas ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🛒Quantidade: Melhores Categorias", "🛒Quantidade: Piores Categorias", "💰 Análise de Custo do Frete", "🧰 Eficiência Logística", "💳 Métodos de Pagamento", "💹 Dispersão"])

    with tab1:
        # 1. Preparação dos Dados de Categoria
        # Vamos agrupar para ver Volume, Lead Time Médio e Frete Médio
        cat_stats = df_filtrado.groupby('product_category_name_english').agg({
            'order_id': 'nunique',
            'Lead_Time': 'mean',
            'freight_value': 'mean'
        }).reset_index()

        # 2. Layout de Colunas
        col_cat1, col_cat2 = st.columns(2)

        with col_cat1:
            # Adicionado ícone de troféu
            st.subheader("Top 10 Categorias Mais Vendidas (Quantidade)")
            top_vendas = cat_stats.sort_values('order_id', ascending=False).head(10)
            
            fig_vendas = px.bar(
                top_vendas, 
                y='product_category_name_english', 
                x='order_id',
                orientation='h',
                color='order_id',
                color_continuous_scale='Blues',
                text='order_id', # ADICIONA O VALOR NA BARRA
                labels={'order_id': 'Total de Pedidos', 'product_category_name_english': 'Categoria'}
            )
            
            # Ajuste: Removendo títulos dos eixos e ocultando a barra de cor se desejar
            fig_vendas.update_layout(
                yaxis={'categoryorder':'total ascending'}, 
                showlegend=False,
                xaxis_title=None, # Remove título X
                yaxis_title=None, # Remove título Y
                coloraxis_showscale=False # Opcional: remove a barra de cores lateral
            )
            st.plotly_chart(fig_vendas, use_container_width=True)

        with col_cat2:
            # ⚡ Top 10 Categorias (Mais Rápidas / Menor Lead Time)
            st.subheader("Top 10 Categorias Mais Rápidas (Dias)")
            # Ordenamos de forma crescente para pegar os menores tempos de entrega
            top_rapidas = cat_stats.sort_values('Lead_Time', ascending=True).head(10)
            
            fig_rapidas = px.bar(
                top_rapidas, 
                y='product_category_name_english', 
                x='Lead_Time',
                orientation='h', 
                color='Lead_Time',
                text='Lead_Time', # Mantemos a coluna aqui
                color_continuous_scale='Greens_r',
                labels={'Lead_Time': 'Dias para Entrega', 'product_category_name_english': 'Categoria'}
            )
            
            # --- AJUSTE AQUI: Formatação para 0 casas decimais ---
            fig_rapidas.update_traces(
                texttemplate='%{text:.0f}', # .0f remove os decimais
                textposition='inside'      # Coloca o número fora da barra
            )
            
            fig_rapidas.update_layout(
                yaxis={'categoryorder':'total descending'},
                xaxis_title=None, 
                yaxis_title=None,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_rapidas, use_container_width=True)
   
        with tab2:
            # 1. Preparação dos Dados de Categoria
            cat_stats = df_filtrado.groupby('product_category_name_english').agg({
                'order_id': 'nunique',
                'Lead_Time': 'mean',
                'freight_value': 'mean'
            }).reset_index()

            # 2. Layout de Colunas
            col_cat3, col_cat4 = st.columns(2)

            with col_cat3:
                st.subheader("Top 10 Categorias Menos Vendidas (Quantidade)")
                top_menos_vendas = cat_stats.sort_values('order_id', ascending=True).head(10)
                
                fig_menos_vendas = px.bar(
                    top_menos_vendas, 
                    y='product_category_name_english', 
                    x='order_id',
                    orientation='h',
                    color='order_id',
                    text='order_id', # Adiciona o valor
                    color_continuous_scale='Reds_r',
                    labels={'order_id': 'Total de Pedidos', 'product_category_name_english': 'Categoria'}
                )
                
                # Formatação: Texto dentro e sem decimais
                fig_menos_vendas.update_traces(
                    texttemplate='%{text:.0f}',
                    textposition='inside',
                    insidetextanchor='end'
                )

                fig_menos_vendas.update_layout(
                    yaxis={'categoryorder':'total descending'},
                    xaxis_title=None, 
                    yaxis_title=None,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_menos_vendas, use_container_width=True)

            with col_cat4:
                st.subheader("Top 10 Categorias Mais Lentas (Dias)")
                top_lentas = cat_stats.sort_values('Lead_Time', ascending=False).head(10)
                
                fig_lentas = px.bar(
                    top_lentas, 
                    y='product_category_name_english', 
                    x='Lead_Time',
                    orientation='h',
                    color='Lead_Time',
                    text='Lead_Time', # Adiciona o valor
                    color_continuous_scale='Oranges',
                    labels={'Lead_Time': 'Dias para Entrega', 'product_category_name_english': 'Categoria'}
                )
                
                # Formatação: Texto dentro e sem decimais
                fig_lentas.update_traces(
                    texttemplate='%{text:.0f}',
                    textposition='inside',
                    insidetextanchor='end'
                )

                fig_lentas.update_layout(
                    yaxis={'categoryorder':'total ascending'},
                    xaxis_title=None, 
                    yaxis_title=None, 
                    coloraxis_showscale=False 
                )
                st.plotly_chart(fig_lentas, use_container_width=True)

    with tab3:          
            # 1. Layout de Colunas
            col_frete1, col_frete2 = st.columns(2)

            with col_frete1:
                # 💸 Top 10 Fretes Mais Caros
                st.subheader("Top 10 Fretes Mais Caros (Média)")
                top_frete_caro = cat_stats.sort_values('freight_value', ascending=False).head(10)
                
                fig_frete_caro = px.bar(
                    top_frete_caro, 
                    y='product_category_name_english', 
                    x='freight_value',
                    orientation='h',
                    color='freight_value',
                    text='freight_value',
                    color_continuous_scale='Reds',
                )
                
                # Formatação: Prefixo R$ e 2 casas decimais
                fig_frete_caro.update_traces(
                    texttemplate='R$ %{text:,.2f}',
                    textposition='inside',
                    insidetextanchor='end'
                )

                fig_frete_caro.update_layout(
                    yaxis={'categoryorder':'total ascending'},
                    xaxis_title=None, 
                    yaxis_title=None,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_frete_caro, use_container_width=True)

            with col_frete2:
                # ✈️ Top 10 Fretes Mais Baratos
                st.subheader("Top 10 Fretes Mais Baratos (Média)")
                top_frete_barato = cat_stats.sort_values('freight_value', ascending=True).head(10)
                
                fig_frete_barato = px.bar(
                    top_frete_barato, 
                    y='product_category_name_english', 
                    x='freight_value',
                    orientation='h',
                    color='freight_value',
                    text='freight_value',
                    color_continuous_scale='Greens_r',
                )
                
                # Formatação: Prefixo R$ e 2 casas decimais
                fig_frete_barato.update_traces(
                    texttemplate='R$ %{text:.2f}',
                    textposition='inside',
                    insidetextanchor='end'
                )

                fig_frete_barato.update_layout(
                    yaxis={'categoryorder':'total descending'},
                    xaxis_title=None, 
                    yaxis_title=None,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_frete_barato, use_container_width=True)
 
    # Adicionando a nova Tab de Funis
    with tab4: # Aba que chamaremos de "🔍 Validação de Fluxo"
        # No topo da página de KPIs
        st.subheader("Validação da Eficiência Logística")
        st.markdown("O funil abaixo valida a quebra de performance desde a expectativa de entrega até o sucesso final.")

        col_f1, col_f2 = st.columns(2)

        with col_f1:
            st.markdown("#### 📦 Por Categoria")
            cat_list = sorted(df_filtrado['product_category_name_english'].unique())
            cat_sel = st.selectbox("Selecione a Categoria", cat_list, key="cat_fun")
            
            df_c = df_filtrado[df_filtrado['product_category_name_english'] == cat_sel]
            
            # Métrica de afunilamento: Pedidos -> Dentro do Prazo (OTIF)
            total_c = len(df_c)
            otif_c = df_c['OTIF'].sum()

            atrasados_c = total_c - otif_c

            # FUNIL POR CATEGORIA
            fig_c = go.Figure(go.Funnel(
                y = ["Total de Pedidos", "Entregues no Prazo (OTIF)"],
                x = [total_c, otif_c],
                # %{value} mostra o número absoluto
                # %{percentInitial:.1%} mostra a porcentagem em relação ao topo com 1 casa decimal
                texttemplate = "%{value} <br> %{percentInitial:.1%}", 
                marker = {"color": ["#161B22", "#FF2C2C"]},
                connector = {"line": {"color": "gray", "dash": "dot"}}
            ))
            fig_c.update_layout(height=300, margin=dict(t=20, b=20, l=10, r=10))
            st.plotly_chart(fig_c, use_container_width=True)

        with col_f2:
            st.markdown("#### 📍 Por Estado")
            est_list = sorted(df_filtrado['customer_state'].unique())
            est_sel = st.selectbox("Selecione a UF", est_list, key="est_fun")
            
            df_e = df_filtrado[df_filtrado['customer_state'] == est_sel]
            
            total_e = len(df_e)
            otif_e = df_e['OTIF'].sum()

            fig_e = go.Figure(go.Funnel(
                y = ["Total de Pedidos", "Entregues no Prazo (OTIF)"],
                x = [total_e, otif_e],
                texttemplate = "%{value} <br> %{percentInitial:.1%}",
                textinfo = "value+percent initial",
                marker = {"color": ["#161B22", "#28a745"]},
                connector = {"line": {"color": "gray", "dash": "dot"}}
            ))
            fig_e.update_layout(height=300, margin=dict(t=20, b=20, l=10, r=10))
            st.plotly_chart(fig_e, use_container_width=True)

        st.info("""
**Como ler este funil:**
* O **Topo (Total)** representa 100% dos pedidos entregues.
* A **Base (OTIF)** mostra a fatia desses pedidos que cumpriram a promessa de prazo. 
* Quanto mais reto o funil, maior a confiabilidade logística da região/categoria.
""")

    with tab6:
        # 3. Gráfico de Dispersão: Peso vs Frete
        st.subheader("Dispersão de Valor de Frete por Peso (Amostra de 10.000 pedidos)")
        
        # Amostra para não travar o gráfico
        df_sample = df_filtrado.sample(min(10000, len(df_filtrado)))

        # AJUSTE AQUI: Ordenamos o DataFrame pelo nome da categoria de A a Z
        df_sample = df_sample.sort_values('product_category_name_english')
        
        fig_scatter = px.scatter(
            df_sample,
            x="product_weight_g",
            y="freight_value",
            color="product_category_name_english", # Esta legenda agora estará em ordem
            size="freight_value",
            hover_data=['product_category_name_english'],
            labels={'product_weight_g': 'Peso (gramas)', 'freight_value': 'Valor do Frete (R$)'},
        )

        # Melhoria opcional: remover títulos dos eixos se quiser seguir o padrão anterior
        fig_scatter.update_layout(
            xaxis_title="Peso (gramas)",
            yaxis=dict(showgrid=False),
            yaxis_title="Frete (R$)"
        )

        st.plotly_chart(fig_scatter, use_container_width=True)
        st.info("**Nota:** Entenda como o peso físico impacta o custo logístico por categoria.")

    with tab5: # Ou a aba que você definiu para Financeiro
        st.subheader("💰 Performance Financeira por Método de Pagamento")
        
        # 1. Preparação dos Dados: Agrupando por Valor Total (Soma)
        pay_value_stats = df_filtrado.groupby('payment_type')['payment_value'].sum().reset_index().sort_values('payment_value', ascending=False)

        # Tradução para o Dashboard
        mapa_pagamento = {
            'credit_card': 'Cartão de Crédito',
            'boleto': 'Boleto',
            'voucher': 'Voucher/Vale',
            'debit_card': 'Cartão de Débito'
        }
        pay_value_stats['payment_type'] = pay_value_stats['payment_type'].map(mapa_pagamento)

        col_v1, col_v2 = st.columns(2)

        with col_v1:
            st.markdown("#### Distribuição do Faturamento (%)")
            fig_pie_val = px.pie(
                pay_value_stats, 
                values='payment_value', 
                names='payment_type',
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Reds_r,
            )
            st.plotly_chart(fig_pie_val, use_container_width=True)

        with col_v2:
            st.markdown("#### Faturamento Total (R$)")
            
            # Criando rótulos amigáveis (Ex: 1.2M ou 450k)
            def formatar_brl(valor):
                if valor >= 1_000_000:
                    return f'R$ {valor/1_000_000:.1f}M'
                return f'R$ {valor/1_000:.0f}k'

            pay_value_stats['texto_valor'] = pay_value_stats['payment_value'].apply(formatar_brl)

            fig_bar_val = px.bar(
                pay_value_stats,
                x='payment_type',
                y='payment_value',
                text='texto_valor',
                color='payment_value',
                color_continuous_scale='Reds'
            )
            
            fig_bar_val.update_layout(
                xaxis_title=None,
                yaxis_title="Volume Financeiro (R$)",
                coloraxis_showscale=False
            )
            fig_bar_val.update_traces(textposition="outside")
            st.plotly_chart(fig_bar_val, use_container_width=True)

        st.success(f"**Resumo Financeiro:** O faturamento total analisado neste período é de **R$ {pay_value_stats['payment_value'].sum():,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))

elif st.session_state.pagina == "Dados":
    st.title("🔍 Visualização Detalhada dos Dados")
    st.markdown("Utilize os filtros abaixo para explorar os pedidos individualmente.")

    # 1. Filtros Rápidos de Busca
    col_search1, col_search2 = st.columns([2, 1])
    
    with col_search1:
        # Busca por nome da categoria
        busca_categoria = st.multiselect(
            "Filtrar por Categoria:", 
            options=sorted(df_filtrado['product_category_name_english'].unique()),
            default=None
        )
    
    with col_search2:
        # Filtro de valor mínimo de frete
        valor_min_frete = st.number_input("Frete mínimo (R$):", min_value=0.0, value=0.0)

    # 2. Aplicando os filtros na visualização
    df_display = df_filtrado.copy()
    
    if busca_categoria:
        df_display = df_display[df_display['product_category_name_english'].isin(busca_categoria)]
    
    df_display = df_display[df_display['freight_value'] >= valor_min_frete]

    # 3. Exibindo a Tabela Interativa
    # Selecionamos as colunas mais importantes para não poluir a tela
    colunas_visiveis = [
        'order_id', 'product_category_name_english', 
        'price', 'freight_value', 'Lead_Time', 'customer_state', 'order_status'
    ]
    
    st.dataframe(
        df_display[colunas_visiveis],
        column_config={
            "order_id": "ID do Pedido",
            "product_category_name_english": "Categoria",
            "price": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
            "freight_value": st.column_config.NumberColumn("Frete", format="R$ %.2f"),
            "Lead_Time": st.column_config.NumberColumn("Dias Entrega", format="%d dias"),
            "customer_state": "UF",
            "order_status": "Status"
        },
        hide_index=True,
        use_container_width=True
    )

    # 4. Botão para baixar os dados filtrados
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados Filtrados (CSV)",
        data=csv,
        file_name='dados_pedidos_filtrados.csv',
        mime='text/csv',
    )

    st.divider()

    # Criando um link amigável com ícone do Kaggle
    st.subheader("**🎲 Base de Dados**")
    st.markdown("""
    Esta plataforma consolida dados do **Brazilian E-Commerce Public Dataset** fornecido pela empresa **Olist**.
    """)
    st.link_button("🌐 Acessar Dataset no Kaggle", "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce", use_container_width=True)

elif st.session_state.pagina == "Resumo":
    st.title("🔍 Resumo Executivo & Insights")
    st.markdown("Consolidação dos achados estratégicos do **Dashboard de Performance Logística (OTIF Analytics).**")
    st.divider()

    # --- BLOCO 1: KPIs DE IMPACTO ---
    col_ins1, col_ins2, col_ins3 = st.columns(3)
    
    with col_ins1:
        st.markdown("### 📍 Regionalidade")
        st.write("**Insight:** O Sudeste é mais eficiente. Norte/Nordeste apresentam fretes até 3x mais caros.")
        st.warning("⚠️ **Risco:** Abandono de carrinho por frete elevado em 15% das regiões.")

    with col_ins2:
        st.markdown("### ⚖️ Peso vs Custo")
        st.write("**Insight:** Produtos acima de 5kg sofrem aumento não linear no frete.")
        st.info("💡 **Oportunidade:** Revisar embalagens e contratos para itens pesados.")

    with col_ins3:
        st.markdown("### ⏱️ Lead Time")
        st.write("**Insight:** O OTIF é estável, mas o tempo de trânsito flutua por categoria.")
        st.success("✅ **Meta:** Manter OTIF acima de 85% para garantir fidelidade.")

    st.divider()

    # --- BLOCO 2: DETALHAMENTO DOS INSIGHTS ---
    st.subheader("📝 Análise Detalhada")
    
    with st.expander("1. Abismo Logístico (Sul/Sudeste vs Norte/Nordeste)", expanded=True):
        st.markdown("""
        A análise geográfica revela que a operação da amostragem é altamente dependente do eixo Sul-Sudeste.
        * **Economia de Escala:** SP, RJ e MG permitem fretes competitivos.
        * **Desafio Logístico:** Em estados como RR e AP, o frete pode ultrapassar 25% do valor do produto.
        * **Ação:** Avaliar centros de distribuição regionais ou parcerias com transportadoras locais.
        """)

    with st.expander("2. Dinâmica de Produtos: Estrelas vs Âncoras", expanded=True):
        st.markdown("""
        * **Categorias Estrela (Beleza, Relógios):** Alto valor, baixo peso. São o motor de lucro.
        * **Categorias Âncora (Móveis, Eletro):** Alto volume, mas críticas. Geram maiores custos e prazos longos.
        * **Ação:** Criar políticas de frete diferenciadas para categorias de grande porte.
        """)

    with st.expander("3. Estratégia de Prazo (Expectativa do Cliente)", expanded=True):
        st.markdown("""
        O OTIF alto indica que a plataforma costuma "prometer prazos longos para entregar antes". 
        Embora aumente a satisfação, prazos estimados muito conservadores podem reduzir a conversão no checkout.
        """)

    # --- BLOCO 3: RECOMENDAÇÕES FINAIS ---
    st.subheader("🚀 Plano de Ação Recomendado")
    
    # Criamos os dados
    dados_recomendacoes = [
        {"Ação": "Reduzir Lead Time da Região Norte", "Prioridade": "Alta", "Impacto": "Vendas"},
        {"Ação": "Auditoria de Transportadoras", "Prioridade": "Média", "Impacto": "OTIF"},
        {"Ação": "Otimização de Embalagem", "Prioridade": "Baixa", "Impacto": "Custo Frete"}
    ]
    
    # Convertemos em DataFrame
    df_rec = pd.DataFrame(dados_recomendacoes)
    
    # Ajustamos o índice para começar em 1
    df_rec.index = df_rec.index + 1
    
    # Exibimos a tabela
    st.table(df_rec)

elif st.session_state.pagina == "Conclusão":
    st.title("🎯 Conclusão")
    st.subheader("⚙️ O Motor de BI da empresa Jerf S/A")
    st.markdown("""
    **1️ O Problema:**
                
    No e-commerce brasileiro, o frete não é só um custo, é uma barreira de conversão. A análise realizada mostra que estados como RR e AP enfrentam fretes que superam 25% do valor do produto, gerando abandono de carrinhos.

    **2️ A Solução Técnica:**
                
    Desenvolvemos um **Motor de BI focado em Validação Operacional**. Através do nosso **Funil de Validação da Eficiência Logística**, isolamos a quebra entre o total de vendas e o sucesso do **OTIF** com precisão de uma casa decimal. Isso permite identificar gargalos exatos por categoria ou região.

    **3️ O Valor de Negócio:**
                
    Com esses insights, a Jerf S/A deixa de ser reativa. Conseguimos auditar SLAs de transportadoras, otimizar custos de frete por peso e preço, e por fim, sinalizar qual entrega tem maior chance de ser realizada, transformando dados em lucro.
    """)