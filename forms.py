from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class CadastroForm(FlaskForm):
    nome_comercio = StringField('Nome do Comércio', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    endereco = StringField('Endereço (Rua, Número, Bairro)', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class EditarComercioForm(FlaskForm):
    nome_comercio = StringField('Nome do Comércio', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    endereco = StringField('Endereço (Rua, Número, Bairro)', validators=[DataRequired()])
    submit = SubmitField('Salvar Alterações')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class ProdutoForm(FlaskForm):
    nome = StringField('Nome do Produto', validators=[DataRequired()])
    preco_original = FloatField('Preço Original (R$)', validators=[DataRequired()])
    preco_desconto = FloatField('Preço com Desconto (R$)', validators=[DataRequired()])
    validade = DateField('Data de Validade', format='%Y-%m-%d', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade Disponível', validators=[DataRequired()])
    imagem = FileField('Imagem do Produto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Somente imagens!')])
    submit = SubmitField('Adicionar Produto')
