from todo_project import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #retorna um usuário com o id fornecido, ou None se não for encontrado


class User(db.Model, UserMixin): #db.Model transforma a classe User em uma tabela para o banco de dados
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # unique nao pode repetir valor
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship('Order',backref='author',lazy=True) # relaciona com pedidos um usuário pode ter muitos pedidos.

    def __repr__(self):
        return f"User('{self.username}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(30),nullable=False,default="Recebido")
    data_pedido = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"order('{self.produto}', '{self.status}')"