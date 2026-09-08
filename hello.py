# Importações de bibliotecas e ferramentas necessárias
import os
from flask import Flask, render_template, redirect, session, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

# Inicialização de Flask e definição de chave secreta
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Chave Forte'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# Classes SQLAlchemy
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

# Facilita carregar os objetos automaticamente no "flask shell"
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

# Criação do formulário e suas definições
class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Rota função view
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        nome = form.name.data

        # Procura a role 'User' no banco, se não existir, cria uma padrão
        user_role = Role.query.filter_by(name='User').first()
        if not user_role:
            user_role = Role(name='User')
            db.session.add(user_role)
            db.session.commit()

        # Cria o usuário associado à role e salva no banco de dados de forma persistente
        usuario = User(username=nome, role=user_role)
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for('index'))

    # Consulta todos os usuários cadastrados no banco para exibir na tabela
    usuarios_cadastrados = User.query.all()
    
    # Pega o último usuário cadastrado para exibir no "Olá, [nome]!"
    ultimo_usuario = User.query.order_by(User.id.desc()).first()
    nome_atual = ultimo_usuario.username if ultimo_usuario else None

    return render_template(
        'index.html', 
        form=form, 
        usuarios=usuarios_cadastrados, 
        name=nome_atual, 
        moment_time=datetime.utcnow()
    )

# Rotas de erro
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)