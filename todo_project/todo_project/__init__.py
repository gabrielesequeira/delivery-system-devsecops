from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__) #criação o objeto da aplicação 
app.config['SECRET_KEY'] = '45cf93c4d41348cd9980674ade9a7356' #assinatura secreta da aplicação 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #referencia ao banco de dados
db = SQLAlchemy(app) #criação do objeto de banco de dados e o associa com a aplicação para criar as tabelas

login_manager = LoginManager(app) #criação do objeto de login manager e o associa com a aplicação para gerenciar as sessões de login dos usuários
login_manager.login_view = 'login' #define a rota de login para redirecionar os usuários não autenticados
login_manager.login_message_category = 'danger'#define a categoria de mensagem para as mensagens de login

bcrypt = Bcrypt(app)#criação do objeto de bcrypt e o associa com a aplicação para fornecer funcionalidades de hashing de senha para proteger as senhas dos usuários no banco de dados

# Always put Routes at end
from todo_project import routes

'''

rotas usadas 
@app.route("/")
@app.route("/login")
@app.route("/about")
@app.route("/register")
@app.route("/logout")
@app.route("/all_orders")
@app.route("/add_order")
@app.route("/update_order/<int:order_id>")
@app.route("/delete_order/<int:order_id>")
@app.route("/account")
@app.route("/account/change_password")

'''