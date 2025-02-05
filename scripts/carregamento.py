import os
import shutil
import pandas as pd
from scripts.utils import send_email
from dotenv import load_dotenv
load_dotenv()

# Fonte dos dados - https://portaldatransparencia.gov.br/download-de-dados/orcamento-despesa
# Dicionário de dados arquivos brutos - https://portaldatransparencia.gov.br/pagina-interna/603417-dicionario-de-dados-orcamento-da-despesa

def carregar_dados():
    try:
        # Lê o arquivo csv da pasta 'arquivos_gold/entrada', move para 'arquivos_gold/lidos', cria as tabelas fatos e dimensões no modelo star schema e 
        # armazena na pasta 'arquivos_gold/processadas', para serem consumidas em excel

        # Diretórios
        gold_entrada = "arquivos_gold/entrada"
        gold_lidos = "arquivos_gold/lidos"
        gold_processadas = "arquivos_gold/processadas"

        # Lê o csv
        fatoOrcamentoDespesa = pd.read_csv(
            gold_entrada + '/fatoOrcamentoDespesa.csv',
            sep=";", 
            encoding="ISO-8859-1", 
            low_memory=False
        )

        # Mover o arquivo csv para a pasta "arquivos_gold/lidos"
        path_gold_entrada = os.path.join(gold_entrada, 'fatoOrcamentoDespesa.csv')
        shutil.move(path_gold_entrada, os.path.join(gold_lidos, 'fatoOrcamentoDespesa.csv'))
        print(f"Movido para {gold_lidos}: fatoOrcamentoDespesa.csv")

        # Criando as tabelas dimensões apartir do arquivo bruto
        dimOrgaoSuperior = fatoOrcamentoDespesa[['cod_orgao_superior', 'nome_orgao_superior']].drop_duplicates()
        dimOrgaoSubordinado = fatoOrcamentoDespesa[['cod_orgao_subordinado', 'nome_orgao_subordinado']].drop_duplicates()
        dimUnidadeOrcamentaria = fatoOrcamentoDespesa[['cod_unidade_orcamentaria', 'nome_unidade_orcamentaria']].drop_duplicates()
        dimFuncao = fatoOrcamentoDespesa[['cod_funcao', 'nome_funcao']].drop_duplicates()
        dimSubFuncao = fatoOrcamentoDespesa[['cod_subfuncao', 'nome_subfuncao']].drop_duplicates()
        dimProgramaOrcamentario = fatoOrcamentoDespesa[['cod_programa_orcamentario', 'nome_programa_orcamentario']].drop_duplicates()
        dimAcao = fatoOrcamentoDespesa[['cod_acao', 'nome_acao']].drop_duplicates()
        dimCategoriaEconomica = fatoOrcamentoDespesa[['cod_categoria_economica', 'nome_categoria_economica']].drop_duplicates()
        dimGrupoDespesa = fatoOrcamentoDespesa[['cod_grupo_despesa', 'nome_grupo_despesa']].drop_duplicates()
        dimElementoDespesa = fatoOrcamentoDespesa[['cod_elemento_despesa', 'nome_elemento_despesa']].drop_duplicates()

        # Selecionando apenas as colunas de interesse para a tabela fato
        fatoOrcamentoDespesa = fatoOrcamentoDespesa[[
                    'ano_exercicio', 
                    'cod_orgao_superior', 
                    'cod_orgao_subordinado', 
                    'cod_unidade_orcamentaria', 
                    'cod_funcao', 
                    'cod_subfuncao', 
                    'cod_programa_orcamentario', 
                    'cod_acao', 
                    'cod_categoria_economica', 
                    'cod_grupo_despesa', 
                    'cod_elemento_despesa', 
                    'orcamento_inicial', 
                    'orcamento_atualizado', 
                    'orcamento_empenhado', 
                    'orcamento_realizado', 
                    'percentual_realizado_orcamento_atualizado', 
                    'origem'
        ]]

        # Salvando as tabelas na pasta arquivos_transformados para serem consumidas no modelo star schema

        # Lista de DataFrames e seus nomes correspondentes
        tables = {
            "dimOrgaoSuperior.xlsx": dimOrgaoSuperior,
            "dimOrgaoSubordinado.xlsx": dimOrgaoSubordinado,
            "dimUnidadeOrcamentaria.xlsx": dimUnidadeOrcamentaria,
            "dimFuncao.xlsx": dimFuncao,
            "dimSubFuncao.xlsx": dimSubFuncao,
            "dimProgramaOrcamentario.xlsx": dimProgramaOrcamentario,
            "dimAcao.xlsx": dimAcao,
            "dimCategoriaEconomica.xlsx": dimCategoriaEconomica,
            "dimGrupoDespesa.xlsx": dimGrupoDespesa,
            "dimElementoDespesa.xlsx": dimElementoDespesa,
            "fatoOrcamentoDespesa.xlsx": fatoOrcamentoDespesa
        }

        # Salvar cada DataFrame na pasta 'arquivos_gold/processadas'
        for filename, table in tables.items():
            file_path = os.path.join(gold_processadas, filename)
            table.to_excel(file_path, index=False)
            
        print('Carregamento concluido com sucesso!')
    except Exception as e:
        # Se der erro, printa a mensagem de erro e envia email
        erro = f"Erro ao executar o carregamento: {e}"
        print(erro)
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
        send_email('rafaelaguida00@gmail.com', EMAIL_PASSWORD, 'rafaelaguida00@gmail.com', 'ERRO ETL - Carregamento', f'{erro}')
        raise
