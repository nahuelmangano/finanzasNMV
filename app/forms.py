
from datetime import date
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, DecimalField, SelectField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Crear cuenta")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")

class CategoryForm(FlaskForm):
    name = StringField("Nombre de categoría", validators=[DataRequired(), Length(max=80)])
    submit = SubmitField("Guardar")

class ExpenseForm(FlaskForm):
    amount = DecimalField("Monto", places=2, rounding=None, validators=[DataRequired(message="Ingresa un monto")])
    occurred_on = DateField("Fecha", default=date.today, validators=[DataRequired()])
    category_id = SelectField("Categoría", coerce=int, validators=[Optional()])
    payment_method = StringField("Método de pago", validators=[Optional(), Length(max=50)])
    description = TextAreaField("Descripción", validators=[Optional(), Length(max=1000)])
    is_fixed = BooleanField("Gasto fijo")
    submit = SubmitField("Guardar")

class ServiceForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(max=120)])
    provider = StringField("Proveedor", validators=[Optional(), Length(max=120)])
    due_day = IntegerField("Día de vencimiento", validators=[Optional(), NumberRange(min=1, max=31)])
    expected_amount = DecimalField("Monto estimado", places=2, validators=[Optional()])
    notes = TextAreaField("Notas", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Guardar")
