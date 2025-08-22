
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    expenses = db.relationship("Expense", backref="user", lazy=True, cascade="all, delete-orphan")
    services = db.relationship("Service", backref="user", lazy=True, cascade="all, delete-orphan")
    categories = db.relationship("Category", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "name", name="uq_user_category_name"),
    )

class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)  # Decimal
    occurred_on = db.Column(db.Date, default=date.today, nullable=False, index=True)
    payment_method = db.Column(db.String(50), nullable=True)  # Efectivo, Tarjeta, Transferencia...
    description = db.Column(db.Text, nullable=True)
    is_fixed = db.Column(db.Boolean, default=False)

    category = db.relationship("Category")

class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    provider = db.Column(db.String(120), nullable=True)
    due_day = db.Column(db.Integer, nullable=True)  # día de vencimiento (1..31)
    expected_amount = db.Column(db.Numeric(12, 2), nullable=True)
    notes = db.Column(db.Text, nullable=True)
