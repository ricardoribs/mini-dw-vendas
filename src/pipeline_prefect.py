from prefect import task, flow
import subprocess
import os

# --- DEFININDO AS TAREFAS (TASKS) ---
# Cada função com @task é um passo que o Prefect monitora.

@task(name="1. Gerar Dados Simulados")
def task_gerar_dados():
    print("🎲 Iniciando Geração de Dados...")
    # O comando check=True faz o Prefect falhar se o script der erro
    subprocess.run(["python", "src/gerar_dados.py"], check=True)

@task(name="2. Ingestão Bronze")
def task_carga_bronze():
    print("🥉 Iniciando Carga Bronze...")
    subprocess.run(["python", "src/carga_bronze.py"], check=True)

@task(name="3. Transformação Silver")
def task_silver():
    print("🥈 Iniciando Transformação Silver...")
    subprocess.run(["python", "src/transformacao_silver.py"], check=True)

@task(name="4. Teste de Qualidade")
def task_qualidade():
    print("yw. 🕵️ Validando Dados...")
    subprocess.run(["python", "src/qualidade_dados.py"], check=True)

@task(name="5. Modelagem Gold")
def task_gold():
    print("🥇 Construindo Camada Gold...")
    subprocess.run(["python", "src/camada_gold.py"], check=True)

# --- DEFININDO O FLUXO (FLOW) ---
# Aqui a gente diz a ordem das coisas.

@flow(name="Pipeline Boticario ETL", log_prints=True)
def fluxo_principal():
    print("🚀 Iniciando Pipeline Automatizado do Mini-DW...")
    
    # Passo 1: Cria os CSVs
    task_gerar_dados()
    
    # Passo 2: Joga no Banco
    task_carga_bronze()
    
    # Passo 3: Limpa
    task_silver()
    
    # Passo 4: Valida (Se falhar aqui, ele para e não roda a Gold)
    task_qualidade()
    
    # Passo 5: Entrega o Final
    task_gold()
    
    print("✨ Pipeline finalizado com sucesso! Pode abrir o Dashboard.")

# --- COMANDO PARA RODAR ---
if __name__ == "__main__":
    fluxo_principal()