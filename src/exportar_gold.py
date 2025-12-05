import duckdb
import os

# Criar pasta Gold se não existir
os.makedirs("data/gold", exist_ok=True)

con = duckdb.connect("mini_dw.duckdb")

print("📦 Exportando tabelas GOLD para CSV...")

# Exportar Fato Vendas
con.execute("COPY (SELECT * FROM fato_vendas) TO 'data/gold/fato_vendas.csv' (HEADER, DELIMITER ',')")
print("✅ fato_vendas.csv gerado.")

# Exportar Dimensão Produto
con.execute("COPY (SELECT * FROM dim_produto) TO 'data/gold/dim_produto.csv' (HEADER, DELIMITER ',')")
print("✅ dim_produto.csv gerado.")

# Exportar Dimensão Cliente
con.execute("COPY (SELECT * FROM dim_cliente) TO 'data/gold/dim_cliente.csv' (HEADER, DELIMITER ',')")
print("✅ dim_cliente.csv gerado.")

con.close()