import streamlit as st
import plotly.express as px
import pandas as pd

st.title("🎓 Finalização e Entrega do Projeto")
st.markdown("Ferramenta desenvolvida como **Projeto Integrador** do curso de **Especialização de Gestão de Projetos** ofertado pelo **Centro Paula Souza**.")
st.divider()

# --- BLOCO 1: KPIs DE IMPACTO ---
col_ins1, col_ins2, col_ins3, col_inst4 = st.columns(4)

with col_ins1:
    st.markdown("### 🏫 Instituição de Ensino")
    st.write("**Centro Paula Souza**")
    st.info("Cidade de São Paulo/SP")
    st.markdown("### 📍 Polo")
    st.write("**Etec Juscelino Kubitschek de Oliveira**")
    st.info("Cidade de Diadema/SP")

with col_ins2:
    st.markdown("### 👨🏽‍🏫 Professores Tutores")
    st.write("**Jean Cláudio Balan**")
    st.info("Professor Mediador")
    st.write("**Marcello Pinotti Meaulo**")
    st.info("Professor de Apoio Presencial do Polo")

with col_ins3:
    st.markdown("### 📚 Nome do Curso")
    st.write("**Especialização em Gestão de Projetos**")
    st.success("TURMA FBK - TO260015545P1")
    st.markdown("### 📁 Nome do Projeto")
    st.write("**Implementação de Dashboard de Performance Logística (OTIF & Lead Time Analytics)**")
    st.success("Projeto Integrador Concluído")

with col_inst4:    
    st.markdown("### 👨🏽‍🎓 Nome do Aluno")
    st.markdown("**Jerfeson Silva Santos**")
    st.success("""
    **Portfólio e Carreira:**
                                    
    Github: [![Github Badge](https://img.shields.io/badge/github-repo-black?style=flat-square&logo=github&link=https://github.com/jerfzz?tab=repositories)](https://github.com/jerfzz?tab=repositories)
                
    LinkedIn: [![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/jerfss/)](https://www.linkedin.com/in/jerfss/)
                
    Streamlit: [![Streamlit Badge](https://img.shields.io/badge/-streamlit-white?style=flat-square&logo=streamlit&logoColor=red&link=https://share.streamlit.io/user/jerfzz)](https://share.streamlit.io/user/jerfzz)                
    """)
    st.markdown("### 📅 Versão do Projeto")
    st.write("**Data:** Junho, 2026")
    st.write("**Versão:** 10.0")

st.divider()

# --- SEÇÃO: PERFORMANCE ACADÊMICA (16 AGENDAS) ---
st.subheader("📈 Histórico de Performance - Ciclo de 16 Agendas")

with st.expander("📊 REVELAR HISTÓRICO DAS MENÇÕES", expanded=False):
    
    # 1. Dados das 16 agendas
    dados_agendas = {
        "Agenda": [f"A{i:02d}" for i in range(1, 17)],
        "Conceito": ["B", "MB", "MB", "MB", "MB", "R", "MB", "MB", "MB", "MB", "MB", "MB", "MB", "B", "MB", "MB"],
        "Menção": [3, 4, 4, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4]
    }
    df_performance = pd.DataFrame(dados_agendas)

    # 2. Gráfico de Linha com o Tema dinâmico
    fig_perf = px.line(
        df_performance, 
        x="Agenda", 
        y="Menção",
        markers=True,
    )

    # Customizando o gráfico para mostrar as letras no eixo Y
    fig_perf.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4],
            ticktext=['I', 'R', 'B', 'MB'],
            range=[0.5, 4.5] # Dá um respiro no gráfico
        ),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Cor da linha (Vermelho Jerf S/A)
    fig_perf.update_traces(line_color='#FF2C2C', marker_size=10)

    st.plotly_chart(fig_perf, use_container_width=True)
    st.info("💡 **Nota do Aluno:** O gráfico acima reflete a dedicação contínua e a evolução técnica ao longo de todo o curso.")

st.divider()

# --- SEÇÃO CONCEITO FINAL ---
st.subheader("🤓 Conceito Final")

# Coluna centralizada para o botão não ficar esticado
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    if st.button("🚀 REVELAR NOTA FINAL", use_container_width=True):
        # Efeito visual de celebração
        st.balloons() 
        
        # Container com estilo personalizado
        st.markdown(
            """
            <div style="
                background-color: BLACK; 
                padding: 20px; 
                border-radius: 15px; 
                text-align: center;
                border: 2px solid white;">
                <h1 style="color: white; margin: 0; font-size: 80px;">MB</h1>
                <p style="color: white; font-weight: bold;">MUITO BOM</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.success("""Parabéns, Jerfeson! Objetivo alcançado com excelência.""")

# Rodapé jogado para fora das colunas para manter o alinhamento correto da página
st.markdown("---")
st.markdown("<p style='text-align: center;'>Jerf S/A Business Intelligence - Todos os direitos reservados © 2026</p>", unsafe_allow_html=True)