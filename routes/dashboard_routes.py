from flask import Blueprint, redirect, render_template, session, url_for
from auth import (
    login_required,
    admin_required,
    empleado_required,
    superadmin_required
)

from models.dashboard import obtenerEmpresa


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


# =====================================================
# DASHBOARD PRINCIPAL
# =====================================================

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    rol = session.get("rol")

    if rol == "ADMIN":
        return redirect(
            url_for("dashboard.dashboard_admin")
        )

    if rol == "SUPERADMIN":
        return redirect(
            url_for("dashboard.dashboard_superadmin")
        )

    if rol == "EMPLEADO":
        return redirect(
            url_for("dashboard.dashboard_user")
        )

    session.clear()

    return redirect(
        url_for("auth.login")
    )


# =====================================================
# DASHBOARD ADMIN
# =====================================================

@dashboard_bp.route("/dashboard_admin")
@login_required
@admin_required
def dashboard_admin():

    id_empresa = session.get("id_empresa")

    if not id_empresa:

        session.clear()

        return redirect(
            url_for("auth.login")
        )


    empresa = obtenerEmpresa(
        id_empresa
    )


    if empresa is None:

        session.clear()

        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "dashboard/dashboard_admin.html",
        empresa=empresa
    )


# =====================================================
# DASHBOARD EMPLEADO
# =====================================================

@dashboard_bp.route("/dashboard_user")
@login_required
@empleado_required
def dashboard_user():

    id_empresa = session.get("id_empresa")

    if not id_empresa:

        session.clear()

        return redirect(
            url_for("auth.login")
        )


    empresa = obtenerEmpresa(
        id_empresa
    )


    if empresa is None:

        session.clear()

        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "dashboard/dashboard_user.html",
        empresa=empresa
    )


# =====================================================
# DASHBOARD SUPERADMIN
# =====================================================

@dashboard_bp.route("/dashboard_superadmin")
@login_required
@superadmin_required
def dashboard_superadmin():

    return render_template(
        "dashboard/dashboard_superadmin.html"
    )