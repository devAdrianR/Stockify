from flask import Blueprint, render_template
from auth import login_required

finanzas_bp = Blueprint("finanzas", __name__)

@finanzas_bp.route("/finanzas")
@login_required
def finanzas():
    return render_template("finanzas/finanzas.html")


@finanzas_bp.route("/registrar_ingreso")
@login_required
def registrar_ingreso():
    return render_template("finanzas/registrar_ingreso.html")


@finanzas_bp.route("/registrar_gasto")
@login_required
def registrar_gasto():
    return render_template("finanzas/registrar_gasto.html")


@finanzas_bp.route("/caja_dia")
@login_required
def caja_dia():
    return render_template("finanzas/caja_dia.html")


@finanzas_bp.route("/cuentas_cobrar")
@login_required
def cuentas_cobrar():
    return render_template("finanzas/cuentas_cobrar.html")


@finanzas_bp.route("/cuentas_pagar")
@login_required
def cuentas_pagar():
    return render_template("finanzas/cuentas_pagar.html")


@finanzas_bp.route("/balance_general")
@login_required
def balance_general():
    return render_template("finanzas/balance_general.html")