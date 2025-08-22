
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Service
from ..forms import ServiceForm

services_bp = Blueprint("services", __name__, template_folder="../templates")

@services_bp.route("/")
@login_required
def index():
    services = Service.query.filter_by(user_id=current_user.id).order_by(Service.name).all()
    return render_template("services/index.html", services=services)

@services_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ServiceForm()
    if form.validate_on_submit():
        s = Service(
            user_id=current_user.id,
            name=form.name.data,
            provider=form.provider.data or None,
            due_day=form.due_day.data,
            expected_amount=form.expected_amount.data,
            notes=form.notes.data or None,
        )
        db.session.add(s)
        db.session.commit()
        flash("Servicio guardado", "success")
        return redirect(url_for("services.index"))
    return render_template("services/create.html", form=form)

@services_bp.route("/delete/<int:service_id>", methods=["POST"])
@login_required
def delete(service_id):
    s = Service.query.filter_by(id=service_id, user_id=current_user.id).first_or_404()
    db.session.delete(s)
    db.session.commit()
    flash("Servicio eliminado", "info")
    return redirect(url_for("services.index"))
