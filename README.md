# BarberUltra 💈

Sistema de agendamento inteligente para barbearias com integração futura ao WhatsApp.

## Visão do Projeto

O objetivo do BarberUltra é permitir que clientes realizem agendamentos diretamente pelo WhatsApp de forma simples e rápida, sem necessidade de cadastro ou instalação de aplicativos.

O sistema será responsável por:

- Gerenciar clientes
- Gerenciar serviços da barbearia
- Gerenciar agendamentos
- Disponibilizar painel administrativo
- Automatizar atendimento via WhatsApp
- Utilizar IA para interpretação de mensagens

## Tecnologias

### Back-end

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

### Infraestrutura

- Docker
- Git
- GitHub

## Estrutura do Projeto

```text
barberultra/
│
├── backend/
│   ├── api/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   └── main.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Funcionalidades Planejadas

### MVP

- [x] Estrutura inicial do projeto
- [x] Configuração do PostgreSQL
- [x] Conexão com banco de dados
- [x] API FastAPI online
- [x] Cadastro de clientes
    - [x] Criar cliente
    - [x] Listar cliente
    - [x] Buscar cliente por id
    - [x] Buscar cliente por telefone
    - [x] Validar telefone duplicado
- [x] Cadastro de serviços
- [ ] Cadastro de agendamentos
- [ ] Consulta de agenda

### Futuro

- [ ] Dashboard administrativo
- [ ] Integração com WhatsApp
- [ ] Confirmação automática de horários
- [ ] Reagendamento automático
- [ ] Assistente com IA
- [ ] Deploy em nuvem

## Como executar

### 1. Clonar repositório

```bash
git clone https://github.com/SEU_USUARIO/barberultra.git
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o arquivo:

```bash
cp .env.example .env
```

Preencha suas credenciais do PostgreSQL.

### 5. Executar

```bash
uvicorn backend.main:app --reload
```

## Status

 Em desenvolvimento

Primeira versão do projeto sendo construída utilizando FastAPI e PostgreSQL.