from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'mydatabase.db')
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    

clientes = []
servicos = ['teste_1', 'teste_2', 'teste_3', 'teste_4']
reservas = []

class Cliente:
    def __init__(self, nome, login, senha, email, telefone):
        self.nome = nome
        self.login = login
        self.senha = senha
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
        nome = request.form['nome']
        login = request.form['login']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']

        # Crie uma nova instância do modelo Usuario
        novo_usuario = Usuario(nome=nome, login=login, email=email, senha=senha, telefone=telefone)

        # Adicione o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

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
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)

