
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Expense, Category
from ..forms import ExpenseForm, CategoryForm

expenses_bp = Blueprint("expenses", __name__, template_folder="../templates")

@expenses_bp.route("/")
@login_required
def index():
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    q = Expense.query.filter_by(user_id=current_user.id)
    if month and year:
        q = q.filter(db.extract("month", Expense.occurred_on) == month,
                     db.extract("year", Expense.occurred_on) == year)
    expenses = q.order_by(Expense.occurred_on.desc()).all()
    total = sum([e.amount for e in expenses]) if expenses else 0
    return render_template("expenses/index.html", expenses=expenses, total=total, month=month, year=year)

@expenses_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ExpenseForm()
    # Load user categories
    cats = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    form.category_id.choices = [(-1, "--- Sin categoría ---")] + [(c.id, c.name) for c in cats]
    if form.validate_on_submit():
        category_id = form.category_id.data if form.category_id.data != -1 else None
        expense = Expense(
            user_id=current_user.id,
            amount=form.amount.data,
            occurred_on=form.occurred_on.data,
            category_id=category_id,
            payment_method=form.payment_method.data or None,
            description=form.description.data or None,
            is_fixed=form.is_fixed.data,
        )
        db.session.add(expense)
        db.session.commit()
        flash("Gasto guardado", "success")
        return redirect(url_for("expenses.index"))
    return render_template("expenses/create.html", form=form)

@expenses_bp.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete(expense_id):
    e = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    db.session.delete(e)
    db.session.commit()
    flash("Gasto eliminado", "info")
    return redirect(url_for("expenses.index"))

@expenses_bp.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    form = CategoryForm()
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    if form.validate_on_submit():
        name = form.name.data.strip()
        exists = Category.query.filter_by(user_id=current_user.id, name=name).first()
        if exists:
            flash("Ya tenés una categoría con ese nombre.", "warning")
        else:
            c = Category(user_id=current_user.id, name=name)
            db.session.add(c)
            db.session.commit()
            flash("Categoría creada.", "success")
            return redirect(url_for("expenses.categories"))
    return render_template("expenses/categories.html", form=form, categories=categories)

@expenses_bp.route("/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    form = ExpenseForm(obj=expense)  # Cargamos datos existentes

    # Cargar categorías del usuario
    cats = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    form.category_id.choices = [(-1, "--- Sin categoría ---")] + [(c.id, c.name) for c in cats]
    if expense.category_id:
        form.category_id.data = expense.category_id

    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.occurred_on = form.occurred_on.data
        expense.category_id = form.category_id.data if form.category_id.data != -1 else None
        expense.payment_method = form.payment_method.data or None
        expense.description = form.description.data or None
        expense.is_fixed = form.is_fixed.data
        db.session.commit()
        flash("Gasto actualizado", "success")
        return redirect(url_for("expenses.index"))

    return render_template("expenses/edit.html", form=form, expense=expense)

