import streamlit as st

st.title("📘 Manual do Usuário — Plataforma Jerf S/A")
st.subheader("Guia Prático de Navegação e Operação do Ecossistema de BI")
st.divider()

# Seção 1: Estrutura do Sistema
st.header("1. Estruturação das Abas (Tabs)")
st.markdown("""
A aplicação está organizada no topo através de guias de navegação rápida:
* **📊 Comparativo de Indicadores Logísticos:** Visão granular em barras exibindo a performance individual de cada métrica por Estado.
* **📈 Evolução do Lead Time Médio (Dias):** Linha temporal de acompanhamento do tempo de resposta logístico.
* **💳 Vendas por Estado / 🟢 Análise Geográfica:** Visões volumétricas e mapas geoespaciais para tomadas de decisão regionalizadas.
""")

st.divider()

# Seção 2: Como Operar os Filtros Reativos (Item 4.2 da EAP)
st.header("2. Operação de Filtros Reativos & Sidebar")
st.markdown("""
No menu lateral esquerdo (Sidebar), você encontrará os seletores globais da plataforma:
1. **Filtro de Período Temporal:** Permite restringir a análise a meses ou anos específicos.
2. **Filtro de Região/Estado:** Ao selecionar ou remover um estado no painel, **todos os gráficos das abas se atualizam instantaneamente** (mecanismo de *Callback Reativo*).
""")

with st.expander("💡 Dica de Ouro para os Filtros"):
    st.info("Para resetar os filtros e voltar a ver o Brasil inteiro, basta clicar no 'X' dos campos de seleção múltipla na barra lateral.")

st.divider()

# Seção 3: O Seletor de Métricas e o Gráfico de Linhas Combinadas
st.header("3. Análise Avançada de KPIs (As 'Bolinhas' de Seleção)")
st.markdown("""
Na aba principal, você possui quatro botões de rádio (seletores circulares) para alternar a visão do painel:

* **🔵 On-Time (Prazo):** Mede o percentual de entregas que chegaram rigorosamente dentro do prazo acordado com o cliente.
* **🟡 In-Full (Qualidade):** Mede o percentual de pedidos que foram entregues completos, sem faltas, trocas ou avarias na mercadoria.
* **🟢 OTIF (Geral):** O indicador final ($OTIF = On\text{-}Time \\times In\text{-}Full$), que representa a eficiência perfeita da entrega.
* **📈 Comparativo de Linhas (KPIs Combinados):** **(Nova Funcionalidade)** Plota as três métricas simultaneamente em um gráfico de linhas para análise de causa-raiz.
""")

# Componente visual simulando uma caixa de alerta do painel (Item 4.4 da EAP)
st.subheader("📋 Interpretando o Painel de Alertas e Cores")
col1, col2, col3 = st.columns(3)
with col1:
    st.error("🟥 Abaixo de 80%: Crítico. Exige plano de ação imediato com as transportadoras ou armazém.")
with col2:
    st.warning("🟨 Entre 80% e 89.9%: Atenção. Região operando abaixo da meta estipulada.")
with col3:
    st.success("🟩 Acima de 90%: Ideal. Região em conformidade com a Meta de Qualidade Jerf S/A.")

st.divider()

# Seção 4: Recursos Visuais Extras
st.header("4. Recursos Interativos do Usuário")
st.markdown("""
* **Seletor de Temas (Item 3.2 da EAP):** No menu de configurações do Streamlit (canto superior direito), é possível alternar entre o **Dark Mode** (melhor para apresentações em telas e projetores) e o **Light Mode** (melhor para leitura de relatórios).
* **Tooltips Dinâmicos (Item 4.6 da EAP):** Ao passar o mouse sobre qualquer ponto das linhas ou barras dos gráficos (função *hover*), uma caixa flutuante detalhada exibirá o valor exato e o nome do Estado avaliado, evitando poluição visual na tela.
""")

st.caption("Manual homologado em conformidade com a Agenda de Encerramento do Projeto. Desenvolvido por Jerfeson Silva Santos.")