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
    return render_template('index.html')

@app.route('/fazer_cadastro', methods=['GET', 'POST'])
def fazer_cadastro():
    if request.method == 'POST':
        # Processar os dados do formulário de cadastro aqui
        
        # Exemplo de cadastro fictício (somente para demonstração)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('fazer_cadastro.html')

@app.route('/logado')
def logado():
    return render_template('logado.html')

@app.route('/esqueci_senha')
def esqueci_senha():
    return render_template('esqueci_senha.html')

@app.route('/fazer_reserva')
def fazer_reserva():
    return render_template('fazer_reserva.html')

@app.route('/editar_reserva')
def editar_reserva():
    return render_template('editar_reserva.html')

@app.route('/cancelar_reserva')
def cancelar_reserva():
    return render_template('cancelar_reserva.html')

@app.route('/opcoes_usuario')
def opcoes_usuario():
    return render_template('opcoes_usuario.html')

@app.route('/meu_perfil')
def meu_perfil():
    return render_template('meu_perfil.html')

@app.route('/logado_admin')
def logado_admin():
    return render_template('logado_admin.html')

@app.route('/gerenciar_cliente')
def gerenciar_cliente():
    return render_template('gerenciar_cliente.html')

@app.route('/gerenciar_servico')
def gerenciar_servico():
    return render_template('gerenciar_servico.html')

@app.route('/gerenciar_horario')
def gerenciar_horario():
    return render_template('gerenciar_horario.html')

@app.route('/gerenciar_reserva')
def gerenciar_reserva():
    return render_template('gerenciar_reserva.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

