from flask import render_template, url_for, flash, redirect, request
from todo_project import app, db, bcrypt
from todo_project.forms import (LoginForm, RegistrationForm, UpdateUserInfoForm,UpdateUserPassword, OrderForm, UpdateOrderForm)
from todo_project.models import User, Order
from flask_login import login_required, current_user, login_user, logout_user
import logging


@app.errorhandler(404)
def error_404(error):
    return (render_template('errors/404.html'), 404)

@app.errorhandler(403)
def error_403(error):
    return (render_template('errors/403.html'), 403)

@app.errorhandler(500)
def error_500(error):
    return (render_template('errors/500.html'), 500)


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_orders'))

    form = LoginForm() #cria uma instância do formulário de login para processar os dados de login enviados pelo usuário. O formulário é usado para validar os dados de entrada e facilitar a autenticação do usuário.
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Check if the user exists and the password is valid
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            logging.info( f'LOGIN_SUCCESS - usuario={user.username}')
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('all_orders'))
        else:
            logging.warning( f'LOGIN_FAILURE - usuario={form.username.data}')
            flash('Falha no Login, check o username e a senha', 'danger')
    
    return render_template('login.html', title='Login', form=form)
    

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logging.info( f'LOGOUT_SUCCESS - usuario={current_user.username}')
    logout_user()
    return redirect(url_for('login'))


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('all_orders'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        logging.info( f'REGISTER_SUCCESS - usuario={user.username}')
        flash(f'Conta criada para {form.username.data}', 'success')
        return redirect(url_for('login'))
    else:
        logging.warning( f'REGISTER_FAILURE - usuario={form.username.data}')

    return render_template('register.html', title='Register', form=form)


@app.route("/all_orders")
@login_required
def all_orders():
    orders = User.query.filter_by(username=current_user.username).first().orders
    return render_template('all_orders.html', title='All orders', orders=orders)


@app.route("/add_order", methods=['POST', 'GET'])
@login_required
def add_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
    produto=form.produto.data,
    quantidade=form.quantidade.data,
    endereco=form.endereco.data,
    author=current_user
)
        db.session.add(order)
        db.session.commit()
        flash('Pedido criado com sucesso!', 'success')
        logging.info(f'ORDER_CREATED - pedido {order.produto} por {current_user.username}')
        return redirect(url_for('all_orders'))
    return render_template('add_order.html', form=form, title='Novo Pedido')


@app.route("/all_orders/<int:order_id>/update_order", methods=['GET', 'POST'])
@login_required
def update_order(order_id):

    order = Order.query.get_or_404(order_id)

    if order.author != current_user:
        flash('Você não possui permissão para alterar este pedido.','danger')
        return redirect(url_for('all_orders'))

    form = UpdateOrderForm()

    if form.validate_on_submit():

        order.produto = form.produto.data
        order.quantidade = form.quantidade.data
        order.endereco = form.endereco.data
        order.status = form.status.data

        db.session.commit()

        logging.info(f"ORDER_UPDATED - pedido {order.id} atualizado por {current_user.username}")

        flash('Pedido atualizado com sucesso!','success')

        return redirect(url_for('all_orders'))

    elif request.method == 'GET':

        form.produto.data = order.produto
        form.quantidade.data = order.quantidade
        form.endereco.data = order.endereco
        form.status.data = order.status

    return render_template('update_order.html',title='Atualizar Pedido',form=form)


@app.route("/all_orders/<int:order_id>/delete_order")
@login_required
def delete_order(order_id):

    order = Order.query.get_or_404(order_id)

    if order.author != current_user:
        flash(
            'Você não possui permissão para excluir este pedido.',
            'danger'
        )
        return redirect(url_for('all_orders'))

    db.session.delete(order)
    db.session.commit()

    logging.warning(f"ORDER_DELETED - pedido {order.id} removido por {current_user.username}")

    flash(
        'Pedido removido com sucesso!',
        'info'
    )

    return redirect(url_for('all_orders'))


@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateUserInfoForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username:  
            current_user.username = form.username.data
            db.session.commit()
            logging.info(f'USERNAME_UPDATED - username atualizado para: {current_user.username}')
            flash('Username Updated Successfully', 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username 

    return render_template('account.html', title='Account Settings', form=form)


@app.route("/account/change_password", methods=['POST', 'GET'])
@login_required
def change_password():
    form = UpdateUserPassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            logging.info(f'PASSWORD_UPDATED - senha atualizada para usuário: {current_user.username}')
            flash('Password Changed Successfully', 'success')
            return redirect(url_for('account'))
        else:
            logging.warning(f'PASSWORD_UPDATE_FAILED - falha ao alterar senha para usuário: {current_user.username}')
            flash('Please Enter Correct Password', 'danger') 

    return render_template('change_password.html', title='Alterar Senha', form=form)


logging.basicConfig(
    filename='delivery.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)