# BarberUltra 💈

Sistema inteligente de agendamento para barbearias com foco em atendimento automatizado via WhatsApp.

## Objetivo

O BarberUltra nasceu para simplificar o processo de agendamento em barbearias, eliminando a necessidade de cadastros, aplicativos adicionais ou atendimento manual para marcação de horários.

A proposta é permitir que o cliente realize todo o processo diretamente pelo WhatsApp, enquanto a barbearia acompanha os agendamentos através de um painel administrativo.

---

## Como Funcionará

### Fluxo do Cliente

1. Cliente envia mensagem para o WhatsApp da barbearia.
2. Sistema identifica o telefone.
3. Caso seja o primeiro contato, solicita o nome.
4. Cliente escolhe o profissional.
5. Cliente escolhe uma data disponível.
6. Cliente escolhe um horário disponível.
7. Cliente escolhe um ou mais serviços.
8. Sistema confirma o agendamento.
9. A agenda do profissional é atualizada automaticamente.

### Fluxo da Barbearia

- Cadastro de profissionais.
- Cadastro de serviços.
- Gerenciamento de disponibilidade.
- Visualização da agenda diária.
- Controle de horários disponíveis.
- Atendimento automatizado via WhatsApp.

---

## Regras de Negócio

### Clientes

- Não existe cadastro tradicional.
- O telefone do WhatsApp identifica o cliente.
- O nome é solicitado apenas no primeiro contato.
- Em contatos futuros, o cliente é reconhecido automaticamente.

### Serviços

- Um agendamento pode possuir múltiplos serviços.
- Cada serviço representa um slot de 30 minutos.

Exemplos:

| Serviços | Tempo Total |
|-----------|------------|
| Corte | 30 min |
| Corte + Barba | 60 min |
| Corte + Barba + Sobrancelha | 90 min |

### Profissionais

- Cada profissional possui sua própria agenda.
- Um profissional pode abrir ou fechar dias específicos para agendamento.
- O cliente escolhe o profissional antes de selecionar os horários.

### Agendamentos

- Um agendamento pertence a um cliente.
- Um agendamento pertence a um profissional.
- Um agendamento pode possuir múltiplos serviços.
- O sistema deverá impedir conflitos de horário.

---

## Tecnologias

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

### Infraestrutura

- Docker
- Git
- GitHub

### Futuras Integrações

- WhatsApp Business API
- Inteligência Artificial
- Dashboard Web

---

## Estrutura do Projeto

```text
barberultra/

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

---

## Funcionalidades Implementadas

### Infraestrutura

- [x] Estrutura inicial do projeto
- [x] Configuração do PostgreSQL
- [x] Integração com FastAPI
- [x] Configuração via arquivo .env

### Clientes

- [x] Criar cliente
- [x] Listar clientes
- [x] Buscar cliente por ID
- [x] Buscar cliente por telefone
- [x] Validação de telefone duplicado

### Serviços

- [x] Criar serviço
- [x] Listar serviços
- [x] Validação de serviço duplicado

### Profissionais

- [x] Criar profissional
- [x] Listar profissionais
- [x] Controle de profissionais ativos

### Agendamentos

- [x] Modelagem da entidade Agendamento
- [x] Modelagem da entidade AgendamentoServico
- [x] Relacionamento entre clientes e serviços
- [x] Relacionamento entre profissionais e agendamentos
- [x] Estrutura inicial da rota de criação de agendamento

---

## Roadmap

### Próxima Sprint

- [ ] Finalizar criação de agendamentos
- [ ] Calcular duração automaticamente
- [ ] Validar conflito de horários
- [ ] Consultar agenda por profissional
- [ ] Consultar horários disponíveis

### Futuras Funcionalidades

- [ ] Dashboard administrativo
- [ ] Agenda visual
- [ ] Integração com WhatsApp
- [ ] Confirmação automática de horários
- [ ] Reagendamento automático
- [ ] Lembretes automáticos
- [ ] Assistente com IA
- [ ] Deploy em nuvem

---

## Como Executar o Projeto

### Clonar o Repositório

```bash
git clone https://github.com/SEU_USUARIO/barberultra.git
```

### Criar Ambiente Virtual

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

Preencha as credenciais do PostgreSQL.

### Executar a API

```bash
uvicorn backend.main:app --reload
```

### Documentação Swagger

```text
http://localhost:8000/docs
```

---

## Status
 Em desenvolvimento

Projeto em construção utilizando FastAPI, PostgreSQL e arquitetura voltada para automação de atendimento e agendamento em barbearias.