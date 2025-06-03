# 🍇 Embrapa Grape Production API

![WIP](https://img.shields.io/badge/WIP-work%20in%20progress-blue)
![MVP](https://img.shields.io/badge/MVP-ativo-success)
[![Deploy on Render](https://img.shields.io/badge/Deploy%20on-Render-3c4dbb?logo=render&logoColor=white)](https://render.com/)


API para consulta de dados públicos do site da Embrapa sobre a produção vitivinícola brasileira. Esta aplicação implementa autenticação, autorização por permissão, cache local e tolerância a falhas para garantir acesso eficiente, seguro e confiável aos dados.

---

## 🧠 Sobre o Projeto

A produção e distribuição de uvas e vinhos no Brasil depende de dados confiáveis e atualizados. O site da Embrapa disponibiliza esses dados publicamente, mas de forma pouco estruturada. Esta API resolve esse problema extraindo, tratando e disponibilizando os dados via uma interface REST padronizada.

A arquitetura segue o modelo **hexagonal (Ports & Adapters)**, isolando o domínio e desacoplando o núcleo da aplicação de frameworks externos, facilitando testes, manutenção e escalabilidade.

### 👥 Consumidores potenciais:
- Usuários finais interessados em dados do setor vitivinícola
- LLMs (Modelos de Linguagem) para geração de insights automatizados
- Distribuidoras de bebidas que precisam acompanhar a produção
- Fazendas de uva buscando dados históricos ou regionais para tomada de decisão

## 📡 URL da API Pública

A API está disponível publicamente no seguinte endpoint:

🌐 **Base URL**: [`https://minha-api.onrender.com`](https://fiap-tech-challenge-nhyz.onrender.com/)

📘 **Documentação Swagger**: [`https://minha-api.onrender.com/docs`](https://fiap-tech-challenge-nhyz.onrender.com/docs)

🔒 A maioria dos endpoints requer autenticação via token JWT no header.


---

## ⚙️ Stack Utilizada

| Tecnologia           | Descrição                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `FastAPI`            | Framework web assíncrono para criação de APIs REST com excelente suporte a OpenAPI |
| `Uvicorn`            | Servidor ASGI leve e rápido para FastAPI                                  |
| `BeautifulSoup4`     | Extração e parsing de HTML dos dados da Embrapa                           |
| `PyJWT`              | Geração e validação de tokens JWT                                         |
| `passlib[bcrypt]`    | Hash de senhas seguro para autenticação                                   |
| `Requests`           | Requisições HTTP síncronas                                                |
| `Pandas`             | Manipulação de dados e estruturação em CSV                                |
| `Deep Translator`    | Tradução automática de dados, se necessário                               |
| `Tenacity`           | Reexecução automática com estratégia de backoff                           |
| `PyBreaker`          | Circuit Breaker para chamadas externas (Ex: site da Embrapa)              |
| `python-json-logger` | Logs estruturados em JSON para produção                                   |
| `Pytest`             | Testes automatizados                                                      |
| `Gunicorn`           | Servidor WSGI/ASGI para ambiente de produção com workers gerenciados      |

---

## 🧭 Como Usar a API (Autenticação e Acesso)

Siga o passo a passo abaixo para consumir os recursos da API com segurança:

### 1. 👤 Criar um novo usuário

Faça uma requisição `POST` para o endpoint `/user/sign-up` com os dados do novo usuário:

    POST /user/sign-up
    Content-Type: application/json

    {
      "id": 123,
      "login": "usuario123",
      "first_name": "João",
      "last_name": "Silva",
      "password": "senhaSegura123",
      "permissions": ["info_production", "info_processing", "info_marketing"]
    }

---

### 2. 🔐 Realizar login e obter o token de acesso

Faça uma requisição `POST` para `/user/log-in` com as credenciais:

    POST /user/log-in
    Content-Type: application/json

    {
      "username": "seu_usuario",
      "password": "sua_senha_segura"
    }

🔁 A resposta incluirá um token JWT no seguinte formato:

    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }

---

### 3. 📥 Inserir o token na autenticação

Você pode usar o token de duas formas:

#### ✅ Opção 1: Usando o Swagger UI (interface `/docs`)

1. Acesse `/docs`
2. Clique no botão **"Authorize"** no topo
3. Preencha com:

       Bearer <seu_token>

4. Clique em **Authorize** e depois **Close**

#### ✅ Opção 2: Usando manualmente via `curl` ou Postman

Inclua o token no cabeçalho da requisição:

    Authorization: Bearer <seu_token>

---

### 4. 📊 Consultar os dados de produção

Com o token JWT válido, agora você pode consumir o endpoint principal:

    GET /info/production?page=1&page_size=10
    Authorization: Bearer <seu_token>

Este endpoint retorna os dados processados da produção de uvas a partir do site da Embrapa.

---

📝 **Observação:** Cada endpoint exige permissões diferentes no payload do JWT. A autorização é feita com base nas permissões associadas ao token.


---

## 🚀 Como Executar o Projeto

### 🔧 Requisitos
- Python 3.10+
- `pip` ou `poetry`
- (opcional) virtualenv

### 💻 Execução Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/embrapa-production-api.git
cd embrapa-production-api

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação localmente
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

### 📦 Execução em Produção

Use o Gunicorn com workers ASGI:

```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:10000
```

---

## 🛡️ Segurança e IAM

O sistema de autenticação está baseado em JWT:

- **Autenticação**: Usuário deve enviar o token no header `Authorization: Bearer <token>`
- **Validação de token**: O token é decodificado, verificado e validado
- **Permissões por endpoint**: Cada rota define a permissão necessária para ser acessada
- **Porta IAM (Input Port)**: O domínio chama a porta de autorização dentro da aplicação, mantendo o isolamento

---

## 🧠 Domínio e Arquitetura

A arquitetura segue o padrão **Hexagonal (Ports & Adapters)**:

- Entradas: HTTP (FastAPI)
- Núcleo: casos de uso, validações e regras de negócio
- Saídas: scraping (Embrapa), cache local, autenticação
- **Isolamento total** entre camadas facilita testes e manutenções

---

## 📂 Cache Inteligente

A aplicação salva uma cópia preprocessada dos dados em formato `.csv` no diretório `resources/cache`, reduzindo chamadas repetidas ao site da Embrapa.

---

## 🔁 Tolerância a Falhas

O consumo do site da Embrapa é protegido por:

- **Retries automáticos com `tenacity`**
- **Circuit Breaker com `pybreaker`**: evita sobrecarregar a fonte de dados em caso de falha contínua

---


## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
