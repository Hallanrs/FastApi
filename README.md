# API de Pedidos com FastAPI

API REST de pedidos de pizzaria, com cadastro de usuários, autenticação JWT e controle de acesso por usuário e admin. Projeto feito acompanhando o curso **Curso de FastAPI - Rest API com Python (Hashtag Programação)**.

## Tecnologias

- FastAPI + Uvicorn
- SQLAlchemy + SQLite (`banco.db`)
- Alembic (migrações)
- passlib/bcrypt (hash de senha)
- python-jose (tokens JWT)

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `main.py` | Cria o `app`, carrega as configurações do `.env` e registra os routers |
| `models.py` | Tabelas do banco: `Usuario`, `Pedidos`, `ItemPedido` |
| `schemas.py` | Schemas Pydantic de entrada e de resposta |
| `dependencies.py` | `pegar_sessao` (sessão do banco) e `verificar_token` (usuário logado) |
| `auth_routes.py` | Rotas `/auth`: cadastro, login e refresh do token |
| `order_routes.py` | Rotas `/pedidos` (todas exigem token) |
| `alembic/` | Migrações do banco |

## Como rodar

Requer Python 3.12.

### 1. Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 3. Configurar o `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=coloque-uma-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Só a `SECRET_KEY` é obrigatória; as outras têm esses valores como padrão. Para gerar uma chave:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Criar o banco de dados

```powershell
alembic upgrade head
```

Isso cria o `banco.db` com as tabelas `usuarios`, `pedidos` e `itens_pedido`.

### 5. Subir a API

```powershell
uvicorn main:app --reload
```

A API fica em http://127.0.0.1:8000 e a documentação interativa em http://127.0.0.1:8000/docs.

## Como usar

1. Crie uma conta em `POST /auth/criar_conta`:
   ```json
   { "nome": "Ana", "email": "ana@email.com", "senha": "123456" }
   ```
2. No `/docs`, clique em **Authorize** e entre com o e-mail (no campo `username`) e a senha. A partir daí o Swagger envia o token em todas as rotas.
3. Fora do Swagger, faça login em `POST /auth/login` e envie o `access_token` no header:
   ```
   Authorization: Bearer <access_token>
   ```

### Rotas

| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/criar_conta` | Cadastra um usuário |
| POST | `/auth/login` | Retorna `access_token` (30 min) e `refresh_token` (7 dias) |
| POST | `/auth/login-form` | Login em formulário, usado pelo botão Authorize do `/docs` |
| GET | `/auth/refresh` | Gera um novo `access_token` (envie o `refresh_token` no header) |
| POST | `/pedidos/pedido` | Cria um pedido (`{ "usuario": <id> }`) |
| POST | `/pedidos/pedido/adicionar-item/{id_pedido}` | Adiciona um item e recalcula o preço |
| POST | `/pedidos/pedido/remover-item/{id_item_pedido}` | Remove um item e recalcula o preço |
| POST | `/pedidos/pedido/finalizar/{id_pedido}` | Muda o status para `FINALIZADO` |
| POST | `/pedidos/pedido/cancelar/{id_pedido}` | Muda o status para `CANCELADO` |
| GET | `/pedidos/pedido/{id_pedido}` | Mostra um pedido com os itens |
| GET | `/pedidos/listar/pedidos-usuario` | Lista os pedidos do usuário logado |
| GET | `/pedidos/listar` | Lista todos os pedidos (só admin) |

Exemplo de item para `adicionar-item`:

```json
{ "quantidade": 2, "sabor": "calabresa", "tamanho": 8, "preco_unitario": 40.0 }
```

### Permissões

- Um usuário só vê e altera os próprios pedidos.
- Um admin vê e altera qualquer pedido e pode usar `/pedidos/listar`.
- O cadastro sempre cria usuários comuns. Para tornar alguém admin, altere direto no banco:
  ```sql
  UPDATE usuarios SET admin = 1 WHERE email = 'ana@email.com';
  ```

## Migrações

Depois de alterar `models.py`, gere e aplique uma nova migração:

```powershell
alembic revision --autogenerate -m "descricao da mudanca"
alembic upgrade head
```
