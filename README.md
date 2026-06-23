# 🍕 Gerenciamento SaaS MVP - Pizzaria Project

Um sistema de backend robusto, escalável e seguro desenvolvido em Python para a gestão de cardápios e pedidos de pizzarias e comércios locais. O projeto foi estruturado sob uma arquitetura de monólito modular flexível, preparando a base para um ecossistema multi-tenant (multi-inquilino) onde cada empresa possui isolamento completo dos seus dados.

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem:** Python 3.11+ (com tipagem estática e *Type Hinting* extensivo)
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (Alta performance, validação automática de dados e documentação interativa com Swagger/OpenAPI)
* **ORM / Base de Dados:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Modelação moderna utilizando `Mapped`, `mapped_column` e relacionamentos tipados)
* **Validação de Dados:** [Pydantic v2](https://docs.pydantic.dev/) (Garantia de integridade de dados na entrada e serialização limpa nas saídas da API)
* **Base de Dados Atual:** SQLite (Para facilidade de desenvolvimento local e portabilidade)

---

## 🔒 Engenharia e Segurança da Informação (OWASP & Boas Práticas)

Como parte dos meus estudos práticos em Segurança da Informação e desenvolvimento seguro, este projeto implementa diversas defesas contra vulnerabilidades comuns descritas pelo OWASP:

* **Prevenção contra IDOR (Insecure Direct Object Reference):** As rotas de manipulação de pedidos (`POST`, `PUT`, `DELETE` e `GET` específicos) validam rigorosamente a propriedade do dado. O sistema garante que um utilizador autenticado só possa aceder, modificar ou cancelar pedidos que pertençam ao seu próprio `user_id`.
* **Mitigação do Problema N+1:** Otimização de consultas relacionais à base de dados utilizando `joinedload`. Em vez de realizar múltiplas consultas em loops (o que degradaria a performance e sobrecarregaria o servidor), a base de dados traz produtos, imagens e dados das empresas vinculadas numa única query otimizada.
* **Arquitetura Baseada em DTO (Data Transfer Objects):** Através dos Schemas do Pydantic (`ResponseModel`), o sistema garante o encapsulamento de informações sensíveis, retornando ao cliente final apenas os dados autorizados e omitindo palavras-passe, tokens ou dados corporativos internos.
* **Autenticação Secura:** Controle de acessos de rotas protegidas utilizando tokens JWT (JSON Web Tokens) e criptografia para armazenamento seguro de palavras-passe.

---

## 🚀 Próximos Passos (Roadmap de Evolução)

O planeamento do projeto está a ser documentado diretamente através das **Issues do GitHub**, englobando as seguintes metas:

- [ ] **Performance:** Migração da base de dados de SQLite para **PostgreSQL** em ambiente de produção.
- [ ] **Infraestrutura:** Dockerização completa da aplicação com `Dockerfile` e `docker-compose` para deploy simplificado.
- [ ] **Otimização de Mídia:** Substituição do armazenamento de imagens em Base64/Blob diretamente na base de dados por uploads para um Object Storage em Nuvem (Ex: AWS S3 ou Supabase Storage), armazenando na base apenas as URLs públicas das imagens.
- [ ] **Filtros Avançados:** Implementação de paginação (`limit` e `offset`) e parâmetros de busca dinâmicos na API de cardápio geral.
- [ ] **Interface Visual:** Desenvolvimento de um painel administrativo multiplataforma utilizando **Flet (Python/Flutter)** para os lojistas gererem os seus produtos.
- [ ] **Comunicação Assíncrona:** Integração em segundo plano (Background Tasks) para envio automático de comprovantes de pedidos para o WhatsApp do cliente.

---

## 📂 Como Configurar e Executar o Projeto Localmente

Siga o passo a passo abaixo para configurar o ambiente de desenvolvimento na sua máquina local:

### 1. Clonar o Repositório

Abra o seu terminal e execute o comando abaixo para descarregar o projeto:

```bash
git clone [https://github.com/mgbrouli/pizzaria-project.git](https://github.com/mgbrouli/pizzaria-project.git)
cd pizzaria-project

```

### 2. Configurar o Ambiente Virtual (venv)
É altamente recomendável utilizar um ambiente virtual isolado para não misturar as dependências do projeto com o sistema global.

No Windows (PowerShell):


```PowerShell

python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux / macOS (Terminal):

```bash
python3 -m venv .venv
source .venv/bin/activate

```

### 3. Instalar as Dependências
Com o seu ambiente virtual devidamente ativo (geralmente indicado por um `(.venv)` no início da linha do terminal), instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente (.env)
O sistema necessita de algumas configurações locais para segurança e tempo de sessão.

Crie um ficheiro com o nome exato de `.env` dentro da pasta `/app/core/` (onde o ficheiro config.py as procura) e configure-o com a estrutura abaixo:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=30 #Quantidade de tempo numerico
SECRET_KEY=sua_chave_secreta_e_segura_aqui 
ALGORITHM=HS256 #Escolher qual algoritmo de criptografia preferir
```


### 5. Iniciar o Servidor de Desenvolvimento
Com tudo configurado, execute o servidor local através do Uvicorn:

```bash
uvicorn app.main:app --reload
```
Se tudo estiver correto, o Uvicorn iniciará com sucesso e começará a monitorizar alterações em tempo real no código.

### 6. Aceder à Documentação da API
Com o servidor a correr, pode testar todas as rotas e regras de negócio diretamente pelo navegador utilizando a interface interativa Swagger UI do FastAPI:

URL do Swagger: http://127.0.0.1:8000/docs
