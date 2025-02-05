import os
import shutil
import glob

# Definição dos diretórios
dir_gold_lidos = "arquivos_gold/lidos"
dir_silver_lidos = "arquivos_silver/lidos"
dir_gold_processadas = "arquivos_gold/processadas"
dir_bronze_lidos = "arquivos_bronze/lidos"
dir_bronze_entrada = "arquivos_bronze/entrada"

# Remover todos os CSVs das pastas lidos
def remover_csv(diretorio):
    arquivos_csv = glob.glob(os.path.join(diretorio, "*.csv"))
    for arquivo in arquivos_csv:
        os.remove(arquivo)
        print(f"Removido: {arquivo}")

# Remover todos os arquivos Excel da pasta processadas
def remover_excel(diretorio):
    arquivos_xlsx = glob.glob(os.path.join(diretorio, "*.xlsx"))
    for arquivo in arquivos_xlsx:
        os.remove(arquivo)
        print(f"Removido: {arquivo}")

# Mover pastas zipadas de arquivos_bronze/lidos para arquivos_bronze/entrada
def mover_zip(diretorio_origem, diretorio_destino):
    arquivos_zip = glob.glob(os.path.join(diretorio_origem, "*.zip"))
    for arquivo in arquivos_zip:
        shutil.move(arquivo, diretorio_destino)
        print(f"Movido: {arquivo} -> {diretorio_destino}")

# Executando as funções
if __name__ == "__main__":
    remover_csv(dir_gold_lidos)
    remover_csv(dir_silver_lidos)
    remover_excel(dir_gold_processadas)
    mover_zip(dir_bronze_lidos, dir_bronze_entrada)

    print("Reset do ambiente concluído!")
