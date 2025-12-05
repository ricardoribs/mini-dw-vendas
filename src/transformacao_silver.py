import duckdb

# 1. Conectar ao banco existente
db_name = "mini_dw.duckdb"
print(f"🔌 Conectando ao banco {db_name}...")
con = duckdb.connect(db_name)

# 2. A Mágica do SQL (Limpeza e Enriquecimento)
# Vamos criar a tabela SILVER_VENDAS juntando tudo numa tabelona só.
# Isso facilita muito análises rápidas.

query_silver = """
CREATE OR REPLACE TABLE silver_vendas AS
SELECT 
    -- 1. Selecionamos e renomeamos o que interessa da tabela de Vendas
    v.id_venda,
    v.id_produto,
    v.id_cliente,
    
    -- 2. Tratamento de Data: O CSV traz como texto, aqui convertemos para DATA/HORA real
    CAST(v.data_venda AS TIMESTAMP) as data_venda,
    
    -- 3. Garantir que valor é numérico
    CAST(v.valor_total AS DECIMAL(10,2)) as valor_total,
    v.quantidade,
    v.canal_venda,
    
    -- 4. Enriquecimento: Trazendo dados do Cliente (JOIN)
    c.nome as nome_cliente,
    c.email as email_cliente,
    c.estado as uf_cliente,
    
    -- 5. Enriquecimento: Trazendo dados do Produto (JOIN)
    p.nome_produto,
    p.categoria as categoria_produto,
    p.linha as linha_produto

FROM bronze_vendas v
-- "LEFT JOIN": Procure o cliente na tabela de clientes usando o id_cliente
LEFT JOIN bronze_clientes c ON v.id_cliente = c.id_cliente
-- "LEFT JOIN": Procure o produto na tabela de produtos usando o id_produto
LEFT JOIN bronze_produtos p ON v.id_produto = p.id_produto

WHERE 
    -- 6. Regra de Qualidade: Só queremos vendas com valor maior que zero
    v.valor_total > 0
"""

print("🧹 Executando a limpeza e criando a tabela SILVER_VENDAS...")
con.execute(query_silver)

# 3. Validar
print("\n🔎 Verificando a nova tabela Silver:")
# Mostrar estrutura
print(con.sql("DESCRIBE silver_vendas").df())

print("\n👀 Amostra dos dados limpos (com nomes e estados):")
con.sql("SELECT id_venda, data_venda, nome_cliente, uf_cliente, nome_produto, valor_total FROM silver_vendas LIMIT 5").show()

# 4. Fechar
con.close()
print("\n✨ Transformação Silver concluída!")