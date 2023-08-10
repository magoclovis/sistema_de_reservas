from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

# Defina classes para Cliente, Servico e Reserva aqui
# Por enquanto, vamos usar dicionários para armazenar os dados

clientes = []
servicos = ['teste_1', 'teste_2', 'teste_3', 'teste_4']
reservas = []

class Cliente:
    def __init__(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone

class Servico:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

class Reserva:
    def __init__(self, cliente, servico):
        self.cliente = cliente
        self.servico = servico

@app.context_processor
def utility_processor():
    def custom_enumerate(seq, start=0):
        return enumerate(seq, start=start)
    
    return dict(enumerate=custom_enumerate)


# Rotas da aplicação
@app.route('/')
def index():
    return render_template('index.html', clientes=clientes)

@app.route('/fazer_cadastro', methods=['GET', 'POST'])
def fazer_reserva():
    if request.method == 'POST':
        # Obtenha dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        servico_id = request.form['servico']

        # Crie um novo cliente se ainda não existir
        cliente = None
        for c in clientes:
            if c.email == email:
                cliente = c
                break
        if cliente is None:
            cliente = Cliente(nome=nome, email=email, telefone=telefone)
            clientes.append(cliente)

        # Agende a reserva
        servico = servicos[int(servico_id)]
        reserva = Reserva(cliente=cliente, servico=servico)
        reservas.append(reserva)

        flash('Cadastro feito com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('fazer_cadastro.html', servicos=servicos)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

