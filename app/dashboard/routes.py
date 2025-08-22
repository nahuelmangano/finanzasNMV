
from datetime import date, timedelta
from collections import defaultdict
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Expense, Category

dashboard_bp = Blueprint("dashboard", __name__, template_folder="../templates")

@dashboard_bp.route("/")
@login_required
def home():
    # Totales del mes actual
    today = date.today()
    month_start = today.replace(day=1)
    q = Expense.query.filter(Expense.user_id == current_user.id,
                             Expense.occurred_on >= month_start,
                             Expense.occurred_on <= today)
    month_expenses = q.all()
    month_total = float(sum([e.amount for e in month_expenses])) if month_expenses else 0.0

    # Totales por categoría del mes
    cat_totals = defaultdict(float)
    for e in month_expenses:
        name = e.category.name if e.category else "Sin categoría"
        cat_totals[name] += float(e.amount)

    # Últimos 6 meses (total por mes)
    series = []
    labels = []
    for i in range(5, -1, -1):
        # Primer día del mes i meses atrás
        y = (today.year * 12 + today.month - 1 - i) // 12
        m = (today.month - 1 - i) % 12 + 1
        start = date(y, m, 1)
        if m == 12:
            end = date(y + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(y, m + 1, 1) - timedelta(days=1)
        total = db.session.query(db.func.coalesce(db.func.sum(Expense.amount), 0)).filter(
            Expense.user_id == current_user.id,
            Expense.occurred_on >= start,
            Expense.occurred_on <= end
        ).scalar()
        labels.append(f"{m:02d}/{y}")
        series.append(float(total or 0))

    # Datos para Chart.js
    cat_labels = list(cat_totals.keys())
    cat_values = [round(v, 2) for v in cat_totals.values()]

    return render_template("dashboard/home.html",
                           month_total=round(month_total, 2),
                           cat_labels=cat_labels,
                           cat_values=cat_values,
                           trend_labels=labels,
                           trend_values=series)
