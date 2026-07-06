from flask import Blueprint, redirect, render_template, session, url_for
from auth import login_required, admin_required, empleado_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    if session["rol"] == "Administrador":
        return redirect(url_for("dashboard.dashboard_admin"))

    return redirect(url_for("dashboard.dashboard_user"))

@dashboard_bp.route("/dashboard_admin")
@login_required
@admin_required
def dashboard_admin():
    return render_template("dashboard/dashboard_admin.html")


@dashboard_bp.route("/dashboard_user")
@login_required
@empleado_required
def dashboard_user():
    return render_template("dashboard/dashboard_user.html")


