from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_bcrypt import Bcrypt
import os
import sqlite3

app = Flask(__name__, template_folder='C:\\Users\\joaov\\Downloads\\sistema_de_reservas\\templates')
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'mydatabase.db')
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'  # Rota para redirecionar em caso de acesso não autorizado

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 

    def set_senha(self, senha):
        self.senha = bcrypt.generate_password_hash(senha).decode('utf-8')

    # método para verificar as credenciais do usuário
    @classmethod
    def verificar_credenciais(cls, login, senha):
        usuario = cls.query.filter_by(login=login).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            return usuario
        return None
    
    is_admin = db.Column(db.Boolean, default=False)

class ReservaDB(db.Model):
    __tablename__ = 'reserva'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    hora_inicio = db.Column(db.String(5), nullable=False)
    servico = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


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
    def __init__(self, cliente, servico, data, hora_inicio):
        self.cliente = cliente
        self.servico = servico
        self.data = data
        self.hora_inicio = hora_inicio

@app.context_processor
def utility_processor():
    def custom_enumerate(seq, start=0):
        return enumerate(seq, start=start)
    
    return dict(enumerate=custom_enumerate)


# Rotas da aplicação
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('logado'))
    
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        if not login or not senha:
            flash('Por favor, preencha todos os campos.', 'error')
        else:
            usuario = Usuario.verificar_credenciais(login, senha)
            if usuario:
                login_user(usuario)
                flash('Login bem-sucedido!', 'success')
                return redirect(url_for('logado'))
            else:
                flash('Credenciais inválidas. Tente novamente.', 'error')

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
        novo_usuario.set_senha(senha)  # Chame o método para gerar o hash da senha
        db.session.add(novo_usuario)
        db.session.commit()

        # Adicione o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('fazer_cadastro.html')

@app.route('/logado', methods=['GET'])
@login_required
def logado():
    return render_template('logado.html')

@app.route('/esqueci_senha')
def esqueci_senha():
    return render_template('esqueci_senha.html')

@app.route('/fazer_reserva', methods=['GET', 'POST'])
@login_required
def fazer_reserva():
    if request.method == 'POST':
        data = request.form['data']
        hora_inicio = request.form['hora_inicio']
        servico = request.form['servico']
        
        # Criar uma nova reserva no banco de dados
        nova_reserva = ReservaDB(usuario_id=current_user.id, data=data, hora_inicio=hora_inicio, servico=servico)
        db.session.add(nova_reserva)
        db.session.commit()
        
        flash('Reserva feita com sucesso!', 'success')
        return redirect(url_for('logado'))  # Redirecione para a página logado

    return render_template('fazer_reserva.html', servicos=servicos)


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

@app.route('/index_admin', methods=['GET', 'POST'])
def index_admin():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return render_template('logado_admin.html')
        else:
            flash('Acesso negado. Você não é um administrador.', 'error')
            return redirect(url_for('index'))
    
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        if not login or not senha:
            flash('Por favor, preencha todos os campos.', 'error')
        else:
            usuario = Usuario.verificar_credenciais(login, senha)
            if usuario and usuario.is_admin:
                login_user(usuario)
                flash('Login bem-sucedido como administrador!', 'success')
                return redirect(url_for('logado_admin'))
            else:
                flash('Credenciais inválidas para administrador. Tente novamente.', 'error')

    return render_template('index_admin.html')
    
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)

