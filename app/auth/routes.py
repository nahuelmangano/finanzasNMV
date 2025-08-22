
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..forms import RegisterForm, LoginForm
from ..models import User
from ..extensions import db

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        if User.query.filter_by(email=email).first():
            flash("Ya existe un usuario con ese email.", "warning")
            return render_template("auth/register.html", form=form)
        user = User(email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Cuenta creada. Ahora podés iniciar sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Bienvenido!", "success")
            next_url = request.args.get("next") or url_for("dashboard.home")
            return redirect(next_url)
        flash("Credenciales inválidas", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))
