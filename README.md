# Northwind Orders App

## Descrição
Este projeto tem como objetivo implementar uma aplicação para inserção de pedidos no banco de dados **Northwind**, utilizando Python e os padrões de arquitetura **MVC** e **DAO**. O foco está na prática de segurança contra SQL Injection, uso de driver de conexão e mapeamento objeto-relacional com ORM (SQLAlchemy). Esse repositório refere-se especificamente ao ORM.

> Atividade prática 2 da disciplina **SPAD02 - Banco de Dados 2**.

## Funcionalidades
- Inserção de pedidos no banco de dados de três formas:
  - [SQL Inseguro (com SQL Injection proposital)](https://github.com/Gabriel-Toti/SPAD02-Lista1-Drive)
  - [SQL Seguro (com parâmetros - `psycopg`)](https://github.com/Gabriel-Toti/SPAD02-Lista1-Drive)
  - ORM (usando SQLAlchemy)
- Relatórios:
  - 📄 **Detalhes de um pedido**: número, data, cliente, vendedor, itens com produto, quantidade e preço.
  - 🏆 **Ranking de funcionários**: total de pedidos e valor vendido por período.

## Tecnologias Utilizadas
- Python 3.12+
- PostgreSQL
- psycopg
- SQLAlchemy
- Sqlacodegen (para gerar modelos)
- Visual Studio Code (opcional para execução)


## Como Executar
1. **Clone o repositório**:
```bash
git clone https://github.com/Gabriel-Toti/SPAD02-Lista1-ORM.git
cd SPAD02-Lista1-ORM

2. Instale as dependências:

pip install -r requirements.txt

3. Configure a conexão com o banco no .env: Preencha os dados da sua conexão PostgreSQL.

4. Execute a aplicação:

python src/main.py

5. Caso tenha problemas para fazer alterações no código (as alterações não são aplicadas), execute o comando:

pip install -e .

Você também pode executar diretamente pelo Visual Studio Code ou outro editor de sua preferência.
