import os
import shutil
import pandas as pd
from utils import send_email
from dotenv import load_dotenv
load_dotenv()

# Fonte dos dados - https://portaldatransparencia.gov.br/download-de-dados/orcamento-despesa
# Dicionário de dados arquivos brutos - https://portaldatransparencia.gov.br/pagina-interna/603417-dicionario-de-dados-orcamento-da-despesa

def transformar_arquivo():
    try:
        # Lê o arquivo csv da pasta 'arquivos_silver/entrada', move para 'arquivos_silver/lidos' e faz algumas transformações. No final armazena em camada gold para ser carregado

        # Diretórios
        silver_entrada = "arquivos_silver/entrada"
        silver_lidos = "arquivos_silver/lidos"
        gold_entrada = "arquivos_gold/entrada"

        # Lê o csv
        fatoOrcamentoDespesa = pd.read_csv(
            silver_entrada + '/fatoOrcamentoDespesa.csv',
            sep=";", 
            encoding="ISO-8859-1", 
            low_memory=False
        )

        # Mover o arquivo csv para a pasta 'arquivos_silver/lidos'
        path_silver_lidos = os.path.join(silver_entrada, 'fatoOrcamentoDespesa.csv')
        shutil.move(path_silver_lidos, os.path.join(silver_lidos, 'fatoOrcamentoDespesa.csv'))
        print(f"Movido para {silver_lidos}: fatoOrcamentoDespesa.csv")

        # Percorre as colunas da lista, para substituir "%" por nada, "," por "." e '.zip' por nada. Depois converte para float
        columns_to_float = [
            'ORÇAMENTO INICIAL (R$)', 
            'ORÇAMENTO ATUALIZADO (R$)', 
            'ORÇAMENTO EMPENHADO (R$)', 
            'ORÇAMENTO REALIZADO (R$)', 
            '% REALIZADO DO ORÇAMENTO (COM RELAÇÃO AO ORÇAMENTO ATUALIZADO)',
            'origem'
        ]

        for col in columns_to_float:
            if col == '% REALIZADO DO ORÇAMENTO (COM RELAÇÃO AO ORÇAMENTO ATUALIZADO)':
                fatoOrcamentoDespesa[col] = fatoOrcamentoDespesa[col].str.replace('%', '').str.replace(',', '.')
            elif col == 'origem':
                fatoOrcamentoDespesa[col] = fatoOrcamentoDespesa[col].str.replace('.zip', '')
            else:
                fatoOrcamentoDespesa[col] = fatoOrcamentoDespesa[col].str.replace(',', '.')

            if col != 'origem':
                fatoOrcamentoDespesa[col] = fatoOrcamentoDespesa[col].astype(float) # Converte para float depois das substituições
            else:
                pass

        # Renomeando as colunas para alinhar com a regra do banco de dados da organizacao
        fatoOrcamentoDespesa = fatoOrcamentoDespesa.rename(columns={
            'EXERCÍCIO': 'ano_exercicio',
            'CÓDIGO ÓRGÃO SUPERIOR': 'cod_orgao_superior',
            'NOME ÓRGÃO SUPERIOR': 'nome_orgao_superior',
            'CÓDIGO ÓRGÃO SUBORDINADO': 'cod_orgao_subordinado',
            'NOME ÓRGÃO SUBORDINADO': 'nome_orgao_subordinado',
            'CÓDIGO UNIDADE ORÇAMENTÁRIA': 'cod_unidade_orcamentaria',
            'NOME UNIDADE ORÇAMENTÁRIA': 'nome_unidade_orcamentaria',
            'CÓDIGO FUNÇÃO': 'cod_funcao',
            'NOME FUNÇÃO': 'nome_funcao',
            'CÓDIGO SUBFUNÇÃO': 'cod_subfuncao',
            'NOME SUBFUNÇÃO': 'nome_subfuncao',
            'CÓDIGO PROGRAMA ORÇAMENTÁRIO': 'cod_programa_orcamentario',
            'NOME PROGRAMA ORÇAMENTÁRIO': 'nome_programa_orcamentario',
            'CÓDIGO AÇÃO': 'cod_acao',
            'NOME AÇÃO': 'nome_acao',
            'CÓDIGO CATEGORIA ECONÔMICA': 'cod_categoria_economica',
            'NOME CATEGORIA ECONÔMICA': 'nome_categoria_economica',
            'CÓDIGO GRUPO DE DESPESA': 'cod_grupo_despesa',
            'NOME GRUPO DE DESPESA': 'nome_grupo_despesa',
            'CÓDIGO ELEMENTO DE DESPESA': 'cod_elemento_despesa',
            'NOME ELEMENTO DE DESPESA': 'nome_elemento_despesa',
            'ORÇAMENTO INICIAL (R$)': 'orcamento_inicial',
            'ORÇAMENTO ATUALIZADO (R$)': 'orcamento_atualizado',
            'ORÇAMENTO EMPENHADO (R$)': 'orcamento_empenhado',
            'ORÇAMENTO REALIZADO (R$)': 'orcamento_realizado',
            '% REALIZADO DO ORÇAMENTO (COM RELAÇÃO AO ORÇAMENTO ATUALIZADO)': 'percentual_realizado_orcamento_atualizado'
        })

        # Armazena o df transformado na pasta 'arquivos_gold/entrada'
        output_path = os.path.join(gold_entrada, "fatoOrcamentoDespesa.csv")
        fatoOrcamentoDespesa.to_csv(output_path, index=False, sep=";", encoding="ISO-8859-1")

        print('Transformação concluida com sucesso!')
    except Exception as e:
        # Se der erro, printa a mensagem de erro e envia email
        erro = f"Erro ao executar a transformação: {e}"
        print(erro)
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
        send_email('rafaelaguida00@gmail.com', EMAIL_PASSWORD, 'rafaelaguida00@gmail.com', 'ERRO ETL - Transformação', f'{erro}')
        raise
