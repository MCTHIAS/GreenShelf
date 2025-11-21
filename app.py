from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Usuario, Produto
from forms import CadastroForm, LoginForm, ProdutoForm, EditarComercioForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from vercel_blob import put, delete


load_dotenv()

# --- CONFIGURAÇÃO DA APLICAÇÃO ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-muito-segura')

DATABASE_URL = os.environ.get('POSTGRES_URL')
if not DATABASE_URL:
    raise RuntimeError("A variável de ambiente POSTGRES_URL não está definida.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- INICIALIZAÇÃO DAS EXTENSÕES ---
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça login para acessar esta página."

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    produtos = Produto.query.order_by(Produto.validade.asc()).all()
    return render_template('index.html', produtos=produtos)

@app.route('/produto/<int:produto_id>')
def detalhe_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template('detalhe_produto.html', produto=produto)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = CadastroForm()
    if form.validate_on_submit():
        novo_usuario = Usuario(
            nome_comercio=form.nome_comercio.data,
            email=form.email.data,
            endereco=form.endereco.data
        )
        novo_usuario.set_password(form.senha.data)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.senha.data):
            login_user(usuario)
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    form = ProdutoForm()
    produtos_do_comercio = Produto.query.filter_by(usuario_id=current_user.id).order_by(Produto.validade.asc()).all()
    return render_template('dashboard.html', form=form, produtos=produtos_do_comercio)

@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = EditarComercioForm()

    if form.validate_on_submit():
        current_user.nome_comercio = form.nome_comercio.data
        current_user.email = form.email.data
        current_user.endereco = form.endereco.data
        db.session.commit()
        flash('Seu perfil foi atualizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    elif request.method == 'GET':
        form.nome_comercio.data = current_user.nome_comercio
        form.email.data = current_user.email
        form.endereco.data = current_user.endereco

    return render_template('editar_perfil.html', form=form)

@app.route('/adicionar_produto', methods=['POST'])
@login_required
def adicionar_produto():
    form = ProdutoForm()
    if form.validate_on_submit():
        imagem_url = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                try:
                    blob_result = put(filename, file.read(), {'access': 'public'})
                    imagem_url = blob_result['url']
                except Exception as e:
                    flash(f'Ocorreu um erro ao fazer o upload da imagem: {e}', 'danger')
                    return redirect(url_for('dashboard'))
            elif file.filename != '':
                flash('Tipo de ficheiro de imagem não permitido.', 'warning')
                return redirect(url_for('dashboard'))

        novo_produto = Produto(
            nome=form.nome.data,
            preco_original=form.preco_original.data,
            preco_desconto=form.preco_desconto.data,
            validade=form.validade.data,
            quantidade=form.quantidade.data,
            imagem=imagem_url,
            usuario_id=current_user.id
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Erro no campo '{field}': {error}", 'danger')
    return redirect(url_for('dashboard'))

# --- ROTA PARA DELETAR PRODUTO ---
@app.route('/deletar_produto/<int:produto_id>', methods=['POST'])
@login_required
def deletar_produto(produto_id):
    produto_para_deletar = Produto.query.get_or_404(produto_id)

    if produto_para_deletar.usuario_id != current_user.id:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('dashboard'))

    if produto_para_deletar.imagem:
        try:
            delete(produto_para_deletar.imagem)
        except Exception as e:
            print(f"Erro ao apagar a imagem do Blob: {e}")

    db.session.delete(produto_para_deletar)
    db.session.commit()

    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/excluir_conta', methods=['POST'])
@login_required
def excluir_conta():
    produtos = Produto.query.filter_by(usuario_id=current_user.id).all()
    for produto in produtos:
        if produto.imagem:
            try:
                delete(produto.imagem)
            except Exception as e:
                print(f"Erro ao apagar a imagem do produto do Blob: {e}")
        db.session.delete(produto)

    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash('A sua conta foi eliminada com sucesso.', 'danger')
    return redirect(url_for('index'))


@app.cli.command("init-db")
def init_db_command():
    """Cria as tabelas do banco de dados."""
    db.create_all()
    print("Banco de dados inicializado com sucesso!")
