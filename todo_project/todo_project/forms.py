from flask_wtf import FlaskForm

# Form Fields
from wtforms import StringField, PasswordField, SubmitField, IntegerField

# Validators
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length,
    ValidationError,
    NumberRange
)

# Models
from todo_project.models import User

from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Register')

    # Check wheather user already exists in the Database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Exists')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class UpdateUserInfoForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField(label='Update Info')

    # Check wheather user already exists in the Database
    def validate_username(self, username):
        if username.data != current_user.username:    
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username Exists')


class UpdateUserPassword(FlaskForm):
    old_password = PasswordField(label='Enter Old Password', validators=[DataRequired()])
    new_password = PasswordField(label='Enter New Password', validators=[DataRequired()])
    submit = SubmitField(label='Change password')


class OrderForm(FlaskForm):
    produto = StringField('Produto',validators=[DataRequired()])
    quantidade = IntegerField('Quantidade',validators=[DataRequired()])
    endereco = StringField('Endereço de Entrega',validators=[DataRequired()])
    submit = SubmitField('Criar Pedido')

class UpdateOrderForm(FlaskForm):
    produto = StringField('Produto',validators=[DataRequired()])
    quantidade = IntegerField('Quantidade',validators=[DataRequired()])
    endereco = StringField('Endereço de Entrega',validators=[DataRequired()])

    status = StringField('Status',validators=[DataRequired()])
    submit = SubmitField('Atualizar Pedido')
