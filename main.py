from scripts.extracao import extrair_arquivos
from scripts.transformacao import transformar_arquivo
from scripts.carregamento import carregar_dados

# Main para executar todo o pipeline do ETL - Extração, transformação e carregamento

if __name__ == "__main__":
    extrair_arquivos()
    transformar_arquivo()
    carregar_dados()

    print("Pipeline executado com sucesso!")
