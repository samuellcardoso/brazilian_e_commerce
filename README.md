# Brazilian e-commerce

## Objetivo
Pipeline de Engenharia de Dados para leitura, transformação, validação, modelagem dimensional e carga de dados do dataset Brazilian E-Commerce, disponibilizado no Kaggle.

## Arquitetura
![Arquitetura do Pipeline](./docs/Arquitetura%20Brazilian%20E-Commerce.png)

## Fluxo Pipeline
1. Download manual dos arquivos CSV disponibilizados no Kaggle
2. Armazenamento dos arquivos originais na camada `raw`
3. Leitura dos arquivos com `read_raw.py`
4. Transformação e modelagem dimensional com Pandas
5. Validação dos dados tratados
6. Persistência das dimensões e da fato na camada `processed`
7. Carga do Data Warehouse no PostgreSQL

## Modelo Dimensional
O Data Warehouse utiliza um modelo estrela composto por:

- `dim_cliente`: informações descritivas dos clientes
- `dim_tempo`: atributos relacionados à data das compras
- `fato_venda`: eventos de vendas e suas métricas

### Chaves
- `cliente_id`: chave da dimensão de clientes e chave estrangeira na fato
- `tempo_id`: chave da dimensão temporal e chave estrangeira na fato
- `venda_id`: chave primária da tabela fato

### Granularidade
Cada registro da `fato_venda` representa um item de um pedido.

### Relacionamentos
```text
dim_cliente ───┐
               ├── fato_venda
dim_tempo ─────┘
```
## Decisões Técnicas
- Os arquivos CSV originais são preservados na camada `raw`
- A camada `processed` contém os dados tratados e padronizados
- O PostgreSQL utiliza `UPSERT` com `ON CONFLICT` para evitar duplicidade de registros
- Credenciais do banco são armazenadas em variáveis de ambiente
- O `main.py` centraliza a orquestração das etapas do pipeline
- As etapas utilizam logging para rastrear execução, falhas e quantidade de registros processados

## Análises SQL
O arquivo `sql/analytics.sql` contém consultas para:

- Faturamento total
- Faturamento mensal
- Faturamento por estado e cidade
- Frete médio por item
- Ticket médio por pedido
- Quantidade de itens por cliente
- Quantidade de pedidos por estado
- Média de itens por pedido
- Top 5 clientes por gasto

## Estrutura das Pastas
```text
brazilian_e_commerce/
├── data_lake/
│   ├── raw/
│   └── processed/
├── sql/
│   └── analytics.sql
├── docs/
│   └── Arquitetura Brazilian E-Commerce.png
├── __init__.py
├── read_raw.py
├── transform.py
├── validate.py
├── db_connection.py
├── load.py
├── main.py
├── logging_config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
## Dataset
O projeto utiliza arquivos do Brazilian E-Commerce Public Dataset by Olist.

Após realizar o download, coloque os seguintes arquivos em `data_lake/raw/`:

- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`

## Tecnologias
- Python
- Pandas
- PostgreSQL
- Psycopg
- python-dotenv
- Git / GitHub

## Como executar
1. Clone o repositório
```bash
git clone git@github.com:samuellcardoso/brazilian_e_commerce.git
```
2. Crie e ative o ambiente virtual
```bash
python -m venv .venv
.venv/Scripts/activate
```
3. Instale as dependências
```bash
pip install -r requirements.txt
```
4. Crie um arquivo `.env` com base no `.env.example`

5. Crie o banco de dados no PostgreSQL 
```sql
CREATE DATABASE olist_dw;
```
6. Execute o pipeline
```bash
python main.py
```
## Melhorias Futuras
- Automatizar a obtenção dos dados
- Implementar testes automatizados
- Otimizar o carregamento no PostgreSQL
- Containerizar o pipeline com Docker
- Migrar o Data Lake e o processamento para AWS
- Adicionar novas dimensões, como produto e vendedor