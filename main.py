from extracao import extrair_arquivos
from transformacao import transformar_arquivo
from carregamento import carregar_dados

# Main para executar todo o pipeline do ETL - Extração, transformação e carregamento

if __name__ == "__main__":
    extrair_arquivos()
    transformar_arquivo()
    carregar_dados()

    print("Pipeline executado com sucesso!")
