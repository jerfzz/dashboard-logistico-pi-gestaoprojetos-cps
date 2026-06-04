# 📊 Dashboard Logístico & Governança de Projetos - Jerf S/A
### Especialização em Gestão de Projetos - Centro Paula Souza (CPS)

Sistema interativo de **Business Intelligence e Governança Corporativa** desenvolvido em **Python com o framework Streamlit**. O ecossistema une ciência de dados aplicada à logística e painéis preditivos de gestão, mapeando indicadores operacionais sob as diretrizes do PMBOK e metodologias ágeis.

---

## 💼 Contexto de Negócio e Objetivos

Este projeto foi desenvolvido para solucionar os desafios de centralização de dados, monitoramento reativo e falta de previsibilidade, cenários recorrentes em departamentos de **Logística, Supply Chain e Escritórios de Projetos (PMO)**. Através da automação em Python, o objetivo é integrar o controle analítico da operação a uma linha de gerenciamento rígida para:

- **Monitoramento de KPIs Logísticos:** Centralização moderna e visualização do OTIF (On Time In Full), Lead Time e frete regionalizado.
- **Identificação de Gargalos Operacionais:** Detecção de atrasos por estado e variações de custo no eixo Sul-Sudeste vs. Norte-Nordeste.
- **Governança e Controle de Projetos:** Gerenciamento de restrições de projetos (Escopo, Tempo e Custo) através de ferramentas preditivas (Caminho Crítico - CPM e Gráfico de Gantt).
- **Otimização e Agilidade:** Integração de uma abordagem híbrida (PMBOK + Scrum), substituindo relatórios estáticos por uma plataforma dinâmica que reduz o tempo de resposta da gestão.

---

## 🧭 Estrutura do Dashboard

O sistema possui navegação lateral (utilizando a nova API `st.Page`) com as seguintes visualizações:

- 🏠 **Home** – Portal de entrada institucional da Jerf S/A  
- 🚚 **Motor de Analytics Logístico (BI)** – Painel analítico de performance de entregas, custos e mapas  
- 📊 **Governança e Gestão (PMBOK)** – Linha de base do projeto, cronograma Gantt e análise do Caminho Crítico (CPM)  
- 📘 **Manual do Usuário** – Documentação e guia de uso das funcionalidades do sistema  
- 🎓 **Projeto Integrador** – Detalhes acadêmicos, escopo e encerramento institucional  

---

## 🔍 Funcionalidades

- **Filtros globais na operação logística por:**
  - Ano e Mês de entrega  
  - Status do pedido  
  - Região e UF (Unidade Federativa)  

- **KPIs Logísticos e Operacionais automáticos:**
  - Faturamento total e Custo total de frete  
  - Índices de OTIF, On-Time e In-Full  
  - Lead Time médio de entrega  

- **Gráficos interativos com Plotly e NetworkX:**
  - Mapas coropléticos de densidade de pedidos e frete por estado  
  - Gráficos de dispersão e funis de eficiência  
  - Cronograma de Gantt dinâmico  
  - Grafo de rede do Caminho Crítico (CPM) com destaque para atividades com folga zero  

- Revisão e simulações de cenários de projetos baseadas em variações de custos e prazos  

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Streamlit**
- **Pandas**
- **Plotly Express & Graph Objects**
- **NetworkX & Matplotlib**

---

## 📊 Base de Dados

O ecossistema consome dados estruturados e relacionais localizados na pasta `data/` provenientes do *Brazilian E-Commerce Public Dataset by Olist*, exigindo os seguintes arquivos:

- `olist_orders_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_products_dataset.csv`
- `product_category_name_translation.csv`
- `brazil-states.geojson` (Malha geográfica na raiz do projeto)

---

## ▶️ Como Executar o Projeto

1️⃣. Clone o repositório:
```bash
git clone [https://github.com/jerfzz/dashboard-logistico-pi-gestaoprojetos.git](https://github.com/jerfzz/dashboard-logistico-pi-gestaoprojetos.git)
```
2️⃣. Instale as dependências:
```bash
pip install -r requirements.txt
```
3️⃣. Execute o aplicativo:
```bash
streamlit run app10.py
```
4️⃣. Acesse no navegador:
```bash
http://localhost:8501
```

###  Projeto publicado através do Streamlit. Acesse-o pelo link

* 🔗 [Streamlit](https://dashboard-logistico-pi-gestaoprojetos-cps.streamlit.app/)

---

## 📈 Principais Insights

- Identificação de gargalos geográficos no Lead Time de entrega para regiões específicas do país.
- Impacto do custo do frete na composição da receita total e margem operacional.
- Identificação precisa das tarefas restritivas (Caminho Crítico) que determinam a duração do projeto em 70 dias.
- Alocação eficiente de recursos e contingência financeira baseada no teto orçamentário estabelecido.

---

## 🎓 Contexto Acadêmico

- Trabalho de Conclusão de Curso (Projeto Integrador) focado na aplicação prática de conceitos de:
- Gestão de Projetos (Metodologias Ágeis e Preditivas)
- Governança Corporativa e PMBOK
- Engenharia de Dados e ETL (Extract, Transform, Load)
- Business Intelligence e Visualização de Dados Interativa

---

## 📁 Estrutura do Projeto

* home.py — Script principal que gerencia o roteamento do app (st.Page)
* views/ — Pasta contendo os módulos de visão (analytics.py, governanca.py, manual.py, projeto_integrador.py)
* data/ — Diretório reservado para os arquivos CSV de dados analíticos
* brazil-states.geojson — Arquivo geoespacial para renderização do mapa de calor do Brasil
* requirements.txt  — Lista de bibliotecas e dependências do projeto para deploy
* README.md  — Documentação do projeto

---

## 📈 Evidências

Seguem algumas evidências do projeto:

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/73c0c073-882b-41fe-9258-3935cbc21d63" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/1f4cf30f-9d5e-4605-ad75-cfa0c48b1cd5" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/2368e7b4-6a03-4eb5-bc4c-262b5474f6c4" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/324738e4-f692-4d23-a4b3-60c47bd76731" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/9863e886-3ecc-4031-b260-12f909b1e9d2" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/fcddd689-a46a-475d-b49a-64144dbc76b6" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/7990305b-0a0d-400f-ad42-442d8193e2ee" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/70671302-a260-46df-ab35-0a3116289e8c" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/f692f180-7710-4a46-a78d-aca242e929ce" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/e70711b6-b4ee-4736-9cb1-5471983e2f74" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/08ec6aac-10a8-4337-a5b1-e4796e5cf45a" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/505eb7f3-13b4-4fce-a3cc-e7ec00e1d9d6" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/913937b7-3cb5-4b53-84e4-a54b0052979f" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/263ec242-aac7-43bc-8541-7575825f03ce" />

---

## 🤝 Agradecimentos

Agradecimento especial aos professores tutores Jean Cláudio Balan e Marcello Pinotti Meaulo, aos colegas de curso e ao Centro Paula Souza pelas orientações, suporte e direcionamento técnico que permitiram a consolidação deste ecossistema.

---

## 👤 Autor

**Jerfeson Silva Santos**

* 🔗 *[LinkedIn](https://www.linkedin.com/in/jerfss/)*
* 💻 *[GitHub / Portfólio](https://github.com/jerfzz?tab=repositories)*
* 🟥 *[Streamlit](https://share.streamlit.io/user/jerfzz)*

---

📌 *Este projeto foi desenvolvido com fins educacionais como Projeto Integrador da ***Especialização em Gestão de Projetos ofertada pelo Centro Paula Souza (CPS).***.
