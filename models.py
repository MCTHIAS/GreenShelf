from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome_comercio = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256))
    endereco = db.Column(db.String(250), nullable=False)
    produtos = db.relationship('Produto', backref='comercio', lazy=True)

    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco_original = db.Column(db.Float, nullable=False)
    preco_desconto = db.Column(db.Float, nullable=False)
    validade = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(256), nullable=True, default='default.png')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)