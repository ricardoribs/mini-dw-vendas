import duckdb

print("🌟 Iniciando construção da Camada GOLD (Modelagem Dimensional)...")

# 1. Conectar ao banco
con = duckdb.connect("mini_dw.duckdb")

# --- CRIANDO DIMENSÃO CLIENTE ---
# Objetivo: Ter uma lista única de clientes e seus atributos
print("🔨 Criando DIM_CLIENTE...")
sql_dim_cliente = """
CREATE OR REPLACE TABLE dim_cliente AS
SELECT DISTINCT
    id_cliente,
    nome_cliente as nome,
    email_cliente as email,
    uf_cliente as estado,
    -- Regra de Negócio: Classificar cliente por "antiguidade" (Exemplo simples)
    CASE 
        WHEN email_cliente LIKE '%@gmail.com' THEN 'Gmail User' 
        ELSE 'Outros' 
    END as categoria_email
FROM silver_vendas;
"""
con.execute(sql_dim_cliente)

# --- CRIANDO DIMENSÃO PRODUTO ---
# Objetivo: Ter uma lista única de produtos
print("🔨 Criando DIM_PRODUTO...")
sql_dim_produto = """
CREATE OR REPLACE TABLE dim_produto AS
SELECT DISTINCT
    id_produto,
    nome_produto,
    categoria_produto as categoria,
    linha_produto as linha
FROM silver_vendas;
"""
con.execute(sql_dim_produto)

# --- CRIANDO TABELA FATO VENDAS ---
# Objetivo: Ter apenas os números e as chaves (IDs) para ligar nas dimensões
print("🔨 Criando FATO_VENDAS...")
sql_fato = """
CREATE OR REPLACE TABLE fato_vendas AS
SELECT
    id_venda,
    id_cliente,
    id_produto,
    data_venda,
    -- Extraindo partes da data para facilitar filtros no Dashboard
    EXTRACT(YEAR FROM data_venda) as ano,
    EXTRACT(MONTH FROM data_venda) as mes,
    EXTRACT(DAY FROM data_venda) as dia,
    quantidade,
    valor_total,
    canal_venda
FROM silver_vendas;
"""
con.execute(sql_fato)

# --- VALIDAÇÃO FINAL (O "Cheiro" do Dashboard) ---
print("\n📊 Simulando um Relatório de Dashboard (Top 3 Categorias que mais vendem):")

query_kpi = """
SELECT 
    p.categoria, 
    SUM(f.valor_total) as receita_total
FROM fato_vendas f
JOIN dim_produto p ON f.id_produto = p.id_produto
GROUP BY p.categoria
ORDER BY receita_total DESC
LIMIT 3
"""
con.sql(query_kpi).show()

con.close()
print("\n✨ Camada GOLD concluída! Seu Data Warehouse está pronto.")