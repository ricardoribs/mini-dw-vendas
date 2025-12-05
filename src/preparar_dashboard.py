import duckdb
import os

print("📊 Preparando 'Tabelão' para o Dashboard...")

con = duckdb.connect("mini_dw.duckdb")

# A Query Mágica: Junta Fato com as Dimensões
query_dashboard = """
COPY (
    SELECT 
        f.id_venda,
        f.data_venda,
        f.ano,
        f.mes,
        f.dia,
        f.quantidade,
        f.valor_total,
        f.canal_venda,
        -- Trazendo nomes em vez de IDs
        p.nome_produto,
        p.categoria,
        p.linha,
        c.nome as nome_cliente,
        c.estado,
        c.categoria_email
    FROM fato_vendas f
    LEFT JOIN dim_produto p ON f.id_produto = p.id_produto
    LEFT JOIN dim_cliente c ON f.id_cliente = c.id_cliente
) TO 'data/gold/dashboard_completo.csv' (HEADER, DELIMITER ',')
"""

con.execute(query_dashboard)
con.close()

print("✅ Arquivo 'dashboard_completo.csv' gerado na pasta data/gold!")