import os
import shutil
import zipfile
import pandas as pd
from scripts.utils import send_email
from dotenv import load_dotenv
load_dotenv()

# Fonte dos dados - https://portaldatransparencia.gov.br/download-de-dados/orcamento-despesa
# Dicionário de dados arquivos brutos - https://portaldatransparencia.gov.br/pagina-interna/603417-dicionario-de-dados-orcamento-da-despesa

def extrair_arquivos():
    # Loop para entrar nas pastas zipadas em 'arquivos_bronze/entrada', ler os arquivos csv de dentro delas, move para a 'pasta arquivos_bronze/lidos' e 
    # concatena todos os arquivos em um único df e armazena na pasta 'arquivos_silver/entrada'

    try:
        # Diretórios
        bronze_entrada = "arquivos_bronze/entrada"
        bronze_lidos = "arquivos_bronze/lidos"
        silver_entrada = "arquivos_silver/entrada"

        df_list = []

        print("Abrindo as pastas zipadas e lendos os arquivos csv...")

        # Loop for para iterar sobre as pastas zipadas
        for zip_file in os.listdir(bronze_entrada):
            zip_path = os.path.join(bronze_entrada, zip_file)
            
            if zip_file.endswith(".zip"):
                with zipfile.ZipFile(zip_path, "r") as z:
                    csv_files = [f for f in z.namelist() if f.endswith(".csv")]
                    
                    if not csv_files:
                        print(f"Nenhum CSV encontrado em {zip_file}")
                        continue
                    
                    for file_name in csv_files:
                        # print(f"Lendo: {file_name}") 
                        with z.open(file_name) as f:
                            try:
                                df = pd.read_csv(f, encoding="ISO-8859-1", sep=";")
                                df["origem"] = zip_file  
                                df_list.append(df)
                            except Exception as e:
                                print(f"Erro ao ler {file_name}: {e}")

                # Mover o arquivo ZIP para a pasta 'arquivos_bronze/lidos'
                shutil.move(zip_path, os.path.join(bronze_lidos, zip_file))
                # print(f"Movido para {bronze_lidos}: {zip_file}")

        # Concatena todos os arquivos em um único df e depois move para a pasta 'arquivos_silver/entrada'
        if df_list:
            fatoOrcamentoDespesa = pd.concat(df_list, ignore_index=True)
            output_path = os.path.join(silver_entrada, "fatoOrcamentoDespesa.csv")
            fatoOrcamentoDespesa.to_csv(output_path, index=False, sep=";", encoding="ISO-8859-1")
            print(f"Concatenação concluída e salva em {output_path}!")
        else:
            print("Nenhum arquivo CSV foi carregado.")
    except Exception as e:
        # Se der erro, printa a mensagem de erro e envia email
        erro = f"Erro ao extrair arquivos: {e}"
        print(erro)
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
        send_email('rafaelaguida00@gmail.com', EMAIL_PASSWORD, 'rafaelaguida00@gmail.com', 'ERRO ETL - Extração', f'{erro}')
        raise
