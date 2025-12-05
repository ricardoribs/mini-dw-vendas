import duckdb
import os

# 1. Configuração
# Caminho onde está o CSV
path_bronze = os.path.join("data", "bronze")
# Nome do nosso banco de dados (será um arquivo novo na pasta raiz)
db_name = "mini_dw.duckdb"

# 2. Conectar ao Banco (se não existir, ele cria sozinho)
print(f"🔌 Conectando ao banco {db_name}...")
con = duckdb.connect(db_name)

# 3. Carregar as tabelas (Ingestão)
# O comando CREATE OR REPLACE TABLE cria a tabela ou substitui se já existir

print("⏳ Carregando tabela VENDAS...")
con.execute(f"CREATE OR REPLACE TABLE bronze_vendas AS SELECT * FROM read_csv_auto('{path_bronze}/vendas.csv')")

print("⏳ Carregando tabela CLIENTES...")
con.execute(f"CREATE OR REPLACE TABLE bronze_clientes AS SELECT * FROM read_csv_auto('{path_bronze}/clientes.csv')")

print("⏳ Carregando tabela PRODUTOS...")
con.execute(f"CREATE OR REPLACE TABLE bronze_produtos AS SELECT * FROM read_csv_auto('{path_bronze}/produtos.csv')")

# 4. Teste Rápido (Ver se carregou mesmo)
print("\n🔎 Verificando se os dados entraram no banco:")
# Vamos contar quantas linhas tem na tabela de vendas
qtd = con.execute("SELECT COUNT(*) FROM bronze_vendas").fetchone()
print(f"Total de linhas em bronze_vendas: {qtd[0]}")

# Mostrar as 5 primeiras linhas só pra gente ver a cara dos dados
print("\n👀 Amostra dos dados:")
con.sql("SELECT * FROM bronze_vendas LIMIT 5").show()

# 5. Fechar conexão
con.close()
print("\n✅ Carga Bronze concluída com sucesso!")