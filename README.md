# 🛍️ Vendas - Mini Data Warehouse & Analytics

Este projeto é uma simulação **End-to-End** de Engenharia de Dados focada no varejo (Vendas Omnichannel). 

O objetivo foi construir um pipeline de dados robusto que ingere dados transacionais, aplica regras de qualidade, modela para Business Intelligence e entrega um Dashboard executivo automatizado.

![Status](https://img.shields.io/badge/Status-Concluído-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)
![DuckDB](https://img.shields.io/badge/DuckDB-OLAP-yellow?style=for-the-badge)
![Prefect](https://img.shields.io/badge/Prefect-Orchestration-white?style=for-the-badge)

---

## 📊 Resultado Final (Dashboard)

O pipeline alimenta um Painel Gerencial no **Looker Studio**, permitindo análise de receita por canal, performance de produtos e geografia.

![Dashboard Preview](./dashboard_final.png)

> **Destaques do Negócio:**
> * Visão unificada de canais (Loja Física, App e Site).
> * Cálculo automatizado de Ticket Médio e KPIs.
> * Monitoramento de meta por Estado (UF).

---

## 🏗️ Arquitetura da Solução

O projeto segue a **Medallion Architecture** (Bronze, Silver, Gold), processada localmente com DuckDB e orquestrada via Prefect.

```mermaid
graph LR
    A[📡 Gerador de Dados (Faker)] -->|Ingestão Raw| B[(🥉 Bronze Layer)]
    B -->|Limpeza & Casting| C[(🥈 Silver Layer)]
    C -->|Validação de Qualidade| D{🕵️ Data Quality Gate}
    D -->|Passou| E[(🥇 Gold Layer - Star Schema)]
    D -->|Falhou| X[❌ Alerta de Erro]
    E -->|Exportação CSV| F[📈 Looker Studio]

    🛠️ Tecnologias e Técnicas
    Categoria	Tecnologia	Detalhes da Implementação
Linguagem	Python 3.12	Scripting e manipulação de arquivos.
Banco de Dados	DuckDB	Banco OLAP local para processamento SQL de alta performance.
Orquestração	Prefect	Gerenciamento de fluxo e dependência de tarefas (Pipeline).
Modelagem	Star Schema	Criação de tabelas Fato e Dimensão na camada Gold.
Qualidade	Pandas	Framework próprio de validação (Null checks, Regras de negócio).
Visualização	Looker Studio	Dashboard interativo com filtros dinâmicos.

📂 Estrutura do Data Lake
O projeto organiza os dados em camadas lógicas para garantir governança:

◾ data/bronze: Dados brutos (vendas.csv, clientes.csv) simulando a extração do sistema de origem.

◾ data/silver: Dados tratados. Correção de tipos (Data/Decimal), remoção de duplicatas e enriquecimento (Joins).

◾ data/gold: Dados prontos para consumo.

◾ fato_vendas: Tabela transacional otimizada.

◾ dim_cliente: Dimensão de perfil e segmentação.

◾ dim_produto: Dimensão de catálogo e categorias.

🚀 Como Executar o Projeto
1. Clonar o repositório
git clone [https://github.com/ricardoribs/mini-dw-vendas.git]
cd mini-dw-boticario

2. Instalar dependências
pip install pandas duckdb faker prefect

3. Rodar o Pipeline (ETL Completo)
Utilize o script do orquestrador para executar todas as tarefas na ordem correta:
python src/pipeline_prefect.py
O output mostrará os logs de execução de cada etapa (Bronze -> Silver -> Gold).

