from todo_project import app, db
from todo_project.models import User, Order

with app.app_context():
    db.create_all()
    print("Banco recriado com sucesso!")