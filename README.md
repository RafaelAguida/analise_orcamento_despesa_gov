# ETL de Orçamento e Despesa Governo Brasileiro - Portal da Transparência

## Fonte

[Portal da Transparência - Download Pastas](https://portaldatransparencia.gov.br/download-de-dados/orcamento-despesa)

[Dicionário de Dados do Arquivo Bruto](https://portaldatransparencia.gov.br/pagina-interna/603417-dicionario-de-dados-orcamento-da-despesa)

---

## 📌 Descrição do Projeto

Este projeto utiliza dados de **Orçamento da Despesa do Governo Brasileiro**, disponíveis no Portal da Transparência (link acima). Foram baixadas 12 pastas zipadas, uma para cada ano desde **2014**, e dentro de cada pasta há um **arquivo CSV** contendo os dados detalhados do orçamento.

O objetivo é realizar um **processo completo de ETL (Extração, Transformação e Carga)**, estruturando os dados em um modelo **Star Schema**. As tabelas são organizadas em **dimensões e fato**, permitindo análises para todas as partes interessadas.

Este projeto simula um cenário realista, onde um usuário insere arquivos em uma pasta de entrada para serem processados automaticamente com base nas regras do negócio. Esses arquivos podem ter origens diversas, como **sistemas internos**, **externos** ou **outras fontes de dados**.

A arquitetura do pipeline segue a estrutura de **camadas Bronze, Silver e Gold**, garantindo o armazenamento do **histórico bruto** para consultas futuras e refinando os dados em cada etapa do processamento.

O ETL conta com uma função de **alertas via e-mail**, notificando em caso de falhas no processamento. As mensagens incluem **detalhes do erro** e ajudam na rápida identificação e resolução do problema.

🔄 Estrutura do Pipeline ETL

O processo é dividido em três etapas principais:

1️⃣ **Extração**

Os arquivos CSV estão contidos em 12 pastas zipadas.

O script extracao.py realiza a leitura desses arquivos em uma pasta de partida que é a arquivos_bronze/entrada e concatena os dados.

O arquivo concatenado é salvo em arquivos_silver/entrada.

As pastas zipadas processadas são movidas para arquivos_bronze/lidos.

2️⃣ **Transformação**

O script transformacao.py carrega o arquivo consolidado de arquivos_silver/entrada.

O arquivo é movido para arquivos_silver/lidos antes do processamento.

As transformações incluem:

- ✅ Renomeação de colunas

- ✅ Correção de tipos de dados

- ✅ Substituição de valores em algumas colunas

O resultado final é salvo em arquivos_gold/entrada.

3️⃣ **Carga**

O script carregamento.py carrega o CSV de arquivos_gold/entrada.

O arquivo carregado é movido para arquivos_gold/lidos.

A partir desse arquivo, são criadas 10 tabelas dimensões e 1 tabela fato.

As tabelas finais (dimensões e fato) são armazenados em arquivos_gold/processadas, estruturadas em um modelo Star Schema.

---

## 📂 Estrutura de Diretórios

```bash
etl_orcamento_despesa_gov/
├── arquivo_power_bi/
├── arquivos_bronze/
│   ├── entrada/  # Pastas zipadas baixadas no site do governo, com CVS dentro de cada uma delas
│   ├── lidos/    # Pastas zipadas processadas
├── arquivos_silver/
│   ├── entrada/  # Arquivo CSV consolidado
│   ├── lidos/    # Arquivos processados
├── arquivos_gold/
│   ├── entrada/      # Arquivo pronto para carga
│   ├── lidos/        # Arquivo já carregado
│   ├── processadas/  # Tabelas finais geradas (dimensões e fato)
├── scripts/          
│   ├── extracao.py      
│   ├── transformacao.py
│   ├── carregamento.py
│   ├── utils.py
│   ├── reset_ambiente.py
├── notebooks_dev/      # Usados para desenvolvimento apenas
│   ├── extracao_dev.ipynb
│   ├── transformacao_dev.ipynb
│   ├── carregamento_dev.ipynb
├── main.py      # Script principal que chama todas as funções do ETL
├── .env  # Configurações sensíveis (senhas, paths, etc.)
```

---

## 🛠 Tecnologias Utilizadas

Python (pandas, zipfile, os, dotenv)

Power BI para análise e visualização de dados

Arquitetura Star Schema para modelagem dos dados

---

## ▶️ Como Executar

Requisitos, você deve ter instalado em sua máquina: Python, alguma IDE (recomendo VSCode) e git.

**Certifique-se de que o Python e Git estão instalados**. Para verificar, crie uma pasta em algum lugar, abra sua IDE, abra a pasta criada pela IDE (VSCode: file > open folder) e execute no terminal:

```bash
python --version
```

Se não estiver instalado, baixe em: https://www.python.org/downloads/

```bash
git --version
```

Se não estiver instalado, execute no terminal:

```bash
winget install --id Git.Git -e --source winget
```

Após garantir que as ferramentas estão instaladas corretamente, execute no terminal:

1. Clone o repositório na pasta criada

```bash
git clone https://github.com/RafaelAguida/analise_orcamento_despesa_gov.git
cd analise_orcamento_despesa_gov
```

2. Crie um ambiente virtual e ative

```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# Se der erro, execute
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

3. Instale as dependências

```bash
pip install -r requirements.txt
```

4. Execute este comando no **PowerShell** dentro da pasta do projeto. Depois, configure o arquivo .env com as credenciais do seu email GMAIL (precisa ser uma senha de aplicativo, senha normal nao funciona via código)

```powershell
@"
EMAIL_LOGIN=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_aplicativo
"@ | Out-File -Encoding utf8 .env
```

5. Reset do ambiente, antes de rodar o pipeline, certifique-se de que os arquivos estejam organizados corretamente. Para isso, execute o comando abaixo

```bash
python scripts/reset_ambiente.py
```

6. Execute o main.py:

```bash
python main.py
```

---

## 📊 Resultados

🚀 11 tabelas geradas no formato **Star Schema**

🔍 Dados prontos para consumo no Power BI

⚡ Automatização do pipeline de ETL

📩 Monitoramento proativo, notificações por e-mail em caso de falha no processo

🖥️ Simulação de cenário realista, o usuário insere arquivos na pasta de entrada, simulando extração de um sistema interno ou externo
