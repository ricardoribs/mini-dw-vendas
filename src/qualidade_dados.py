import duckdb
import pandas as pd

print("🕵️ Iniciando Auditoria de Qualidade de Dados (Motor Próprio)...")

# 1. Conectar e pegar os dados da Silver
con = duckdb.connect("mini_dw.duckdb")
df = con.execute("SELECT * FROM silver_vendas").fetchdf()
con.close()

print(f"📊 Analisando {len(df)} linhas de vendas...\n")

total_erros = 0

# --- FUNÇÃO AUXILIAR PARA VALIDAR ---
def validar(regra_nome, condicao_sucesso):
    global total_erros
    if condicao_sucesso:
        print(f"✅ {regra_nome}: PASSOU")
    else:
        print(f"❌ {regra_nome}: FALHOU")
        total_erros += 1

# --- REGRAS DE NEGÓCIO ---

# Regra 1: Verificar se existe algum ID nulo
qtd_nulos = df['id_venda'].isnull().sum()
validar("ID Venda não nulo", qtd_nulos == 0)

# Regra 2: Verificar se existe algum valor menor ou igual a zero
qtd_negativos = df[df['valor_total'] <= 0].shape[0]
validar("Valor Total > 0", qtd_negativos == 0)

# Regra 3: Verificar datas nulas
qtd_datas_ruins = df['data_venda'].isnull().sum()
validar("Data Venda Válida", qtd_datas_ruins == 0)

# Regra 4: Verificar Estados (UF) inválidos
estados_validos = ["SP", "RJ", "MG", "RS", "PR", "BA", "SC", "GO", "PE", "CE", "PA", "MA", "MT", "ES", "AM", "PB", "RN", "AL", "PI", "SE", "RO", "TO", "MS", "AC", "AP", "RR", "DF"]
# Pega os estados únicos que estão nos dados e vê se algum NÃO está na lista oficial
estados_nos_dados = df['uf_cliente'].unique()
estados_errados = [uf for uf in estados_nos_dados if uf not in estados_validos]

validar("Sigla UF Válida", len(estados_errados) == 0)

# --- RESUMO ---
print("\n" + "="*30)
if total_erros == 0:
    print("🏆 SUCESSO! Dados aprovados para a camada Gold.")
else:
    print(f"⚠️ ALERTA! Encontramos {total_erros} falhas.")
print("="*30)