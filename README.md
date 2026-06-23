# 🍕 Projeto Pizzaria / Cardápio SaaS MVP

Um sistema de backend robusto e seguro desenvolvido em Python para gerenciamento de cardápios e pedidos de pizzarias e comércios varejistas. O projeto foi desenhado sob uma arquitetura de microsserviços/monólito modular flexível, permitindo o isolamento de dados por empresa (Multi-Tenant).

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

- **Linguagem:** Python 3.11+ (com Type Hinting extensivo)
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (Alta performance e documentação nativa com Swagger/OpenAPI)
- **ORM / Banco de Dados:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Sintaxe moderna baseada em `Mapped` e `mapped_column`)
- **Validação de Dados:** [Pydantic v2](https://docs.pydantic.dev/) (Garantia de integridade de dados e serialização de respostas)
- **Banco de Dados Atual:** SQLite (Ambiente de desenvolvimento leve e portátil)

---

## 🔒 Engenharia e Segurança da Informação (OWASP & Boas Práticas)

Como estudante de Segurança da Informação, o projeto foi desenvolvido com forte foco em mitigar vulnerabilidades comuns em sistemas web:

* **Prevenção contra IDOR (Insecure Direct Object Reference):** As rotas de edição, deleção de produtos e manipulação de pedidos validam estritamente se o ID da entidade pertence à empresa (`enterprise_id`) ou ao usuário autenticado antes de executar qualquer transação no banco.
* **Autenticação Segura:** Implementação de controle de acesso baseado em tokens JWT para proteção de rotas administrativas.
* **Otimização de Consultas (Performance):** Uso do método `joinedload` do SQLAlchemy nas consultas relacionais para mitigar o problema clássico do **N+1**, reduzindo drasticamente as requisições ao banco de dados em laços de repetição.
* **Arquitetura Limpa:** Separação de responsabilidades utilizando o padrão DTO (Data Transfer Objects) através dos Schemas do Pydantic, impedindo o vazamento de dados sensíveis do banco para o cliente final.

---

## 🚀 Próximos Passos (Roadmap de Evolução)

O planejamento do projeto está organizado através das **Issues do GitHub** e engloba:

- [ ] **Performance:** Migração do banco de dados de SQLite para **PostgreSQL**.
- [ ] **Infraestrutura:** Dockerização completa da aplicação com `Dockerfile` e `docker-compose`.
- [ ] **Otimização:** Substituição do armazenamento de imagens em Base64/Blob por links de um Object Storage em Nuvem (Ex: AWS S3 ou Supabase Storage).
- [ ] **Filtros Avançados:** Implementação de paginação (`limit` e `offset`) e filtros dinâmicos na API de cardápio geral.
- [ ] **Frontend:** Desenvolvimento de um painel administrativo utilizando **Flet (Python/Flutter)** para o gerenciamento das lojas.
- [ ] **Comunicação:** Integração assíncrona (Background Tasks) para envio de comprovantes de pedidos direto para o WhatsApp do cliente.

---

## 📂 Como Executar o Projeto Localmente (Em breve via Docker)

1. Clone o repositório:
   ```bash
   git clone [https://github.com/mgbrouli/pizzaria-project.git](https://github.com/mgbrouli/pizzaria-project.git)
