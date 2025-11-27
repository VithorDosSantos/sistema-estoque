# Sistema de Estoque

Sistema simples de gerenciamento de estoque em Python com Flask.

## Funcionalidades

✅ Adicionar produtos (nome, quantidade e valor obrigatórios - ID gerado automaticamente)
✅ Listar todos os produtos
✅ Listar produtos em ordem alfabética
✅ Comprar produtos com verificação de disponibilidade
✅ Confirmação de compra com atualização automática do estoque

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

## Deploy no Render

1. Faça login no [Render](https://render.com)
2. Clique em "New +" e selecione "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: estoque-app (ou o nome que preferir)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Clique em "Create Web Service"

O Render fará o deploy automaticamente!

## Estrutura do Projeto

```
atividade 5/
├── app.py              # Aplicação principal
├── templates/
│   └── index.html      # Interface web
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
