import streamlit as st

# 1. CONFIGURAÇÃO GLOBAL ÚNICA
st.set_page_config(
    page_title="Plataforma Corporativa - Jerf S/A",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicialização do Estado Global de Tema (Se o seu código usar)
if 'tema_escuro' not in st.session_state:
    st.session_state.tema_escuro = False


# 3. FUNÇÃO QUE RENDERIZA A SUA CAPA PERSONALIZADA
def renderizar_capa():
    st.title("🏢 Plataforma Integrada de Governança e Analytics")
    st.subheader("Bem-vindo ao Ecossistema Corporativo da Jerf S/A")
    st.divider()

    # Grid de Destaques (3 Colunas)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Governança & PMBOK")
        st.info("Acesse o ciclo completo de 16 agendas da Especialização Técnica. Controle de cronograma (CPM), custos, EAP e matrizes de risco.")

    with col2:
        st.markdown("### 🚚 Logística & BI")
        st.success("Explore o motor de Business Intelligence. Análise em tempo real de indicadores cruciais como **OTIF** e **Lead Time** de faturamento.")

    with col3:
        st.markdown("### 🎓 Projeto Integrador")
        st.warning("Trabalho de Conclusão de Curso (TAF) desenvolvido para a Especialização Técnica in Gestão de Projetos — Centro Paula Souza.")

    st.divider()

    # Seção de Contexto do Negócio
    st.markdown("""
    ### 🚀 Contexto do Ecossistema
    Este sistema foi desenvolvido utilizando dados reais do e-commerce brasileiro para solucionar dores de visibilidade operacional. 
    Através do menu lateral, você pode navegar entre a **camada de gestão e planejamento estratégico** e a **camada operacional de ciência de dados**.

    * **Desenvolvedor:** Jerfeson Silva Santos
    * **Orientação:** Prof. Jean Cláudio Balan & Prof. Marcello Pinotti Meaulo
    * **Conceito de Homologação:** MB (Muito Bom) 🏆
    """)

    st.success("Utilize a barra de navegação à esquerda para alternar entre os módulos de Gestão e BI!")


# 4. DECLARAÇÃO DAS PÁGINAS (Usando a pasta alternativa 'views')
page_home = st.Page(
    renderizar_capa, # <-- Passamos a função da capa aqui!
    title="Início",
    icon="🏠",
    default=True
)

page_governanca = st.Page(
    "view/governanca.py", 
    title="Governança e Gestão (PMBOK)", 
    icon="📊"
)

page_analytics = st.Page(
    "view/analytics.py", 
    title="Motor de Analytics Logístico (BI)", 
    icon="🚚"
)

page_manual = st.Page(
    "view/manual.py",
    title="Manual do Usuário",
    icon="📘"
)

page_projeto_integrador = st.Page(
    "view/projeto_integrador.py",
    title="Projeto Integrador",
    icon="🎓"
)


# 5. ORQUESTRACAO DO MENU
pg = st.navigation({
    "Home": [page_home],
    "Módulos do Projeto": [page_governanca, page_analytics, page_manual, page_projeto_integrador]
})

# 6. EXECUÇÃO
pg.run()
