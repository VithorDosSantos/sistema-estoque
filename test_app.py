import pytest
import json
from app import app, produtos, adicionar_produto, listar_produtos, listar_produtos_alfabetica, comprar_produto, confirmar_compra


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def limpar_produtos():
    produtos.clear()
    global proximo_id
    import app as app_module
    app_module.proximo_id = 1
    yield
    produtos.clear()


def test_adicionar_produto():
    produto = adicionar_produto("Teste", 10, 100.0)
    assert produto['id'] == 1
    assert produto['produto'] == "Teste"
    assert produto['quantidade'] == 10
    assert produto['valor'] == 100.0
    assert len(produtos) == 1


def test_listar_produtos():
    adicionar_produto("Produto A", 5, 50.0)
    adicionar_produto("Produto B", 10, 100.0)
    lista = listar_produtos()
    assert len(lista) == 2
    assert lista[0]['produto'] == "Produto A"
    assert lista[1]['produto'] == "Produto B"


def test_listar_produtos_alfabetica():
    adicionar_produto("Zebra", 5, 50.0)
    adicionar_produto("Apple", 10, 100.0)
    adicionar_produto("Mouse", 15, 75.0)
    lista = listar_produtos_alfabetica()
    assert len(lista) == 3
    assert lista[0]['produto'] == "Apple"
    assert lista[1]['produto'] == "Mouse"
    assert lista[2]['produto'] == "Zebra"


def test_comprar_produto_disponivel():
    adicionar_produto("Notebook", 10, 2500.0)
    resultado = comprar_produto(1, 3)
    assert resultado['disponivel'] is True
    assert resultado['produto'] == "Notebook"
    assert resultado['quantidade'] == 3
    assert resultado['total'] == 7500.0


def test_comprar_produto_indisponivel():
    adicionar_produto("Mouse", 5, 50.0)
    resultado = comprar_produto(1, 10)
    assert resultado['disponivel'] is False
    assert resultado['quantidade_disponivel'] == 5
    assert resultado['quantidade_solicitada'] == 10


def test_comprar_produto_inexistente():
    resultado = comprar_produto(999, 1)
    assert resultado is None


def test_confirmar_compra_sucesso():
    adicionar_produto("Teclado", 20, 150.0)
    sucesso = confirmar_compra(1, 5)
    assert sucesso is True
    assert produtos[0]['quantidade'] == 15


def test_confirmar_compra_estoque_insuficiente():
    adicionar_produto("Monitor", 3, 800.0)
    sucesso = confirmar_compra(1, 5)
    assert sucesso is False
    assert produtos[0]['quantidade'] == 3


def test_confirmar_compra_produto_inexistente():
    sucesso = confirmar_compra(999, 1)
    assert sucesso is False


def test_api_get_produtos(client):
    adicionar_produto("Produto API", 10, 100.0)
    response = client.get('/api/produtos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['produto'] == "Produto API"


def test_api_get_produtos_alfabetica(client):
    adicionar_produto("Zebra", 5, 50.0)
    adicionar_produto("Apple", 10, 100.0)
    response = client.get('/api/produtos/alfabetica')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data[0]['produto'] == "Apple"
    assert data[1]['produto'] == "Zebra"


def test_api_criar_produto(client):
    response = client.post('/api/produtos',
                          data=json.dumps({'produto': 'Novo Produto', 'quantidade': 15, 'valor': 200.0}),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['produto'] == 'Novo Produto'
    assert data['quantidade'] == 15


def test_api_criar_produto_incompleto(client):
    response = client.post('/api/produtos',
                          data=json.dumps({'produto': 'Incompleto'}),
                          content_type='application/json')
    assert response.status_code == 400


def test_api_comprar_disponivel(client):
    adicionar_produto("Produto Compra", 10, 100.0)
    response = client.post('/api/comprar',
                          data=json.dumps({'id': 1, 'quantidade': 3}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['disponivel'] is True
    assert data['total'] == 300.0


def test_api_comprar_indisponivel(client):
    adicionar_produto("Produto Limitado", 2, 50.0)
    response = client.post('/api/comprar',
                          data=json.dumps({'id': 1, 'quantidade': 5}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['disponivel'] is False


def test_api_confirmar_compra(client):
    adicionar_produto("Produto Confirmar", 10, 100.0)
    response = client.post('/api/confirmar-compra',
                          data=json.dumps({'id': 1, 'quantidade': 3}),
                          content_type='application/json')
    assert response.status_code == 200
    assert produtos[0]['quantidade'] == 7


def test_api_index(client):
    response = client.get('/')
    assert response.status_code == 200
