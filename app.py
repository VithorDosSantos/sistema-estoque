from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

produtos = []
proximo_id = 1


def adicionar_produto(nome, quantidade, valor):
    global proximo_id
    produto = {
        'id': proximo_id,
        'produto': nome,
        'quantidade': int(quantidade),
        'valor': float(valor)
    }
    produtos.append(produto)
    proximo_id += 1
    return produto


def listar_produtos():
    return produtos


def listar_produtos_alfabetica():
    return sorted(produtos, key=lambda x: x['produto'])


def comprar_produto(produto_id, quantidade_compra):
    for produto in produtos:
        if produto['id'] == produto_id:
            if produto['quantidade'] >= quantidade_compra:
                total = produto['valor'] * quantidade_compra
                return {
                    'disponivel': True,
                    'produto': produto['produto'],
                    'quantidade': quantidade_compra,
                    'valor_unitario': produto['valor'],
                    'total': total
                }
            else:
                return {
                    'disponivel': False,
                    'produto': produto['produto'],
                    'quantidade_disponivel': produto['quantidade'],
                    'quantidade_solicitada': quantidade_compra
                }
    return None


def confirmar_compra(produto_id, quantidade_compra):
    for produto in produtos:
        if produto['id'] == produto_id:
            if produto['quantidade'] >= quantidade_compra:
                produto['quantidade'] -= quantidade_compra
                return True
    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    return jsonify(listar_produtos())


@app.route('/api/produtos/alfabetica', methods=['GET'])
def get_produtos_alfabetica():
    return jsonify(listar_produtos_alfabetica())


@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    data = request.json
    if not data.get('produto') or not data.get('quantidade') or not data.get('valor'):
        return jsonify({'erro': 'Nome, quantidade e valor são obrigatórios'}), 400

    produto = adicionar_produto(data['produto'], data['quantidade'], data['valor'])
    return jsonify(produto), 201


@app.route('/api/comprar', methods=['POST'])
def comprar():
    data = request.json
    produto_id = data.get('id')
    quantidade = data.get('quantidade')

    if not produto_id or not quantidade:
        return jsonify({'erro': 'ID do produto e quantidade são obrigatórios'}), 400

    resultado = comprar_produto(int(produto_id), int(quantidade))

    if resultado is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    return jsonify(resultado)


@app.route('/api/confirmar-compra', methods=['POST'])
def confirmar():
    data = request.json
    produto_id = data.get('id')
    quantidade = data.get('quantidade')

    if not produto_id or not quantidade:
        return jsonify({'erro': 'ID do produto e quantidade são obrigatórios'}), 400

    sucesso = confirmar_compra(int(produto_id), int(quantidade))

    if sucesso:
        return jsonify({'mensagem': 'Compra confirmada com sucesso!'})
    else:
        return jsonify({'erro': 'Não foi possível confirmar a compra'}), 400


if __name__ == '__main__':
    adicionar_produto("Notebook", 10, 2500.00)
    adicionar_produto("Mouse", 50, 45.90)
    adicionar_produto("Teclado", 30, 150.00)

    app.run(debug=True, host='0.0.0.0', port=5000)
