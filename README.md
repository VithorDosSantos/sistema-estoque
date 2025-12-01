# Sistema de Estoque

Sistema simples de gerenciamento de estoque em Python com Flask, incluindo pipeline de CI/CD com qualidade de software.

## Funcionalidades

✅ Adicionar produtos (nome, quantidade e valor obrigatórios - ID gerado automaticamente)
✅ Listar todos os produtos
✅ Listar produtos em ordem alfabética
✅ Comprar produtos com verificação de disponibilidade
✅ Confirmação de compra com atualização automática do estoque

## Pipeline de CI/CD

O projeto inclui um pipeline completo com:

### 🔍 Stage 1: Lint (Qualidade de Código)
- **Flake8**: Verifica estilo de código e problemas sintáticos
- **Pylint**: Análise estática de código com score mínimo de 7.0

### 🧪 Stage 2: Test (Testes Unitários)
- **Pytest**: 17 testes unitários cobrindo todas as funcionalidades
- **Coverage**: Relatório de cobertura de código

### ✅ Stage 3: Quality (Qualidade de Software)
- **Coverage Check**: Garante mínimo de 80% de cobertura
- **Bandit**: Análise de segurança do código

## Como executar localmente

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o aplicativo:
```bash
python app.py
```

3. Acesse: http://localhost:5000

## Executar Testes

```bash
# Testes unitários
pytest test_app.py -v

# Testes com cobertura
pytest test_app.py --cov=app --cov-report=html

# Linting
flake8 app.py --max-line-length=120
pylint app.py
```

## Deploy no Render

1. Faça login no [Render](https://render.com)
2. Clique em "New +" e selecione "Web Service"
3. Conecte seu repositório GitHub/GitLab
4. Configure:
   - **Name**: estoque-app (ou o nome que preferir)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Clique em "Create Web Service"

## Estrutura do Projeto

```
atividade 5/
├── app.py              # Aplicação principal
├── test_app.py         # Testes unitários
├── templates/
│   └── index.html      # Interface web
├── .gitlab-ci.yml      # Pipeline CI/CD
├── .pylintrc           # Configuração Pylint
├── .flake8             # Configuração Flake8
├── requirements.txt    # Dependências
└── README.md          # Documentação
```

## API Endpoints

- `GET /` - Interface web
- `GET /api/produtos` - Lista todos os produtos
- `GET /api/produtos/alfabetica` - Lista produtos em ordem alfabética
- `POST /api/produtos` - Adiciona novo produto
- `POST /api/comprar` - Verifica disponibilidade de compra
- `POST /api/confirmar-compra` - Confirma a compra e atualiza estoque

## Tecnologias

- **Backend**: Python 3.13 + Flask
- **Testes**: Pytest + Coverage
- **Linting**: Flake8 + Pylint
- **Segurança**: Bandit
- **Deploy**: Gunicorn + Render
- **CI/CD**: GitLab CI
