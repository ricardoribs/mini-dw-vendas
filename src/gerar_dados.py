import pandas as pd
import random
from faker import Faker
import os
from datetime import datetime, timedelta

# 1. Configuração Inicial
fake = Faker('pt_BR')  # Isso garante nomes e endereços brasileiros
Faker.seed(42)         # Para gerar sempre os mesmos dados (bom para testes)

# Caminho onde vamos salvar os arquivos
# ../data/bronze significa: "volte uma pasta e entre em data/bronze"
OUTPUT_PATH = os.path.join("data", "bronze")

# Garantir que a pasta existe
os.makedirs(OUTPUT_PATH, exist_ok=True)

print("🚀 Iniciando a simulação de dados do Mini-DW Boticário...")

# --- A. GERAR PRODUTOS (SIMULAÇÃO DE CADASTRO) ---
categorias = {
    'Perfumaria': ['Malbec', 'Floratta', 'Egeo', 'Quasar', 'Glamour'],
    'Cabelos': ['Shampoo Match', 'Condicionador Match', 'Máscara Capilar'],
    'Corpo e Banho': ['Loção Nativa SPA', 'Óleo Corporal', 'Sabonete Líquido'],
    'Maquiagem': ['Batom Make B.', 'Base Mate', 'Máscara de Cílios']
}

lista_produtos = []
id_prod = 1

for categoria, linhas in categorias.items():
    for linha in linhas:
        # Criamos algumas variações para cada linha
        for i in range(1, 4): 
            preco_base = random.uniform(30.0, 250.0)
            lista_produtos.append({
                'id_produto': id_prod,
                'nome_produto': f"{linha} - Variação {i}",
                'categoria': categoria,
                'linha': linha,
                'preco_unitario': round(preco_base, 2)
            })
            id_prod += 1

df_produtos = pd.DataFrame(lista_produtos)
df_produtos.to_csv(os.path.join(OUTPUT_PATH, 'produtos.csv'), index=False)
print(f"✅ Arquivo 'produtos.csv' gerado com {len(df_produtos)} itens.")


# --- B. GERAR CLIENTES ---
qtd_clientes = 500  # Vamos criar 500 clientes falsos
lista_clientes = []

for _ in range(qtd_clientes):
    perfil = fake.simple_profile()
    lista_clientes.append({
        'id_cliente': fake.uuid4(),  # Um ID único e complexo
        'nome': perfil['name'],
        'email': perfil['mail'],
        'estado': fake.state_abbr(), # Sigla do estado (SP, RJ, MA...)
        'data_cadastro': fake.date_between(start_date='-2y', end_date='today')
    })

df_clientes = pd.DataFrame(lista_clientes)
df_clientes.to_csv(os.path.join(OUTPUT_PATH, 'clientes.csv'), index=False)
print(f"✅ Arquivo 'clientes.csv' gerado com {qtd_clientes} clientes.")


# --- C. GERAR VENDAS (A TABELA FATO) ---
qtd_vendas = 2000 # Vamos simular 2000 vendas
lista_vendas = []

# Opções de canais de venda
canais = ['Loja Física', 'App', 'Site', 'Revendedora']

for i in range(qtd_vendas):
    # Escolhe um cliente e um produto aleatório das listas que criamos acima
    cliente_aleatorio = random.choice(lista_clientes)
    produto_aleatorio = random.choice(lista_produtos)
    
    # Quantidade comprada (1 a 5 itens)
    qtd = random.randint(1, 5)
    
    # Data da venda (últimos 365 dias)
    data_venda = fake.date_time_between(start_date='-1y', end_date='now')

    lista_vendas.append({
        'id_venda': i + 1000,
        'id_cliente': cliente_aleatorio['id_cliente'],
        'id_produto': produto_aleatorio['id_produto'],
        'data_venda': data_venda.strftime("%Y-%m-%d %H:%M:%S"),
        'quantidade': qtd,
        'valor_total': round(produto_aleatorio['preco_unitario'] * qtd, 2),
        'canal_venda': random.choice(canais)
    })

df_vendas = pd.DataFrame(lista_vendas)
df_vendas.to_csv(os.path.join(OUTPUT_PATH, 'vendas.csv'), index=False)
print(f"✅ Arquivo 'vendas.csv' gerado com {qtd_vendas} registros de venda.")

print("\n✨ Processo finalizado! Confira a pasta data/bronze.")