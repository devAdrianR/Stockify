from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth import login_required
import mysql.connector as mysql
from config import DB_CONFIG
from models import gastos


finanzas_bp = Blueprint("finanzas", __name__)


@finanzas_bp.route("/finanzas")
@login_required
def finanzas():
    return render_template("finanzas/finanzas.html")


@finanzas_bp.route("/registrar_ingreso")
@login_required
def registrar_ingreso():
    return render_template("finanzas/registrar_ingreso.html")


@finanzas_bp.route("/registrar_gasto", methods=["GET", "POST"])
@login_required
def registrar_gasto():

    if request.method == "POST":

        concepto = request.form.get("concepto", "").strip()
        monto = request.form.get("monto", "").strip()
        categoria = request.form.get("categoria", "").strip()
        fecha = request.form.get("fecha", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        # Validar concepto
        if not concepto:
            flash("El concepto es obligatorio.", "error")
            return redirect(url_for("finanzas.registrar_gasto"))

        # Validar monto
        if not monto:
            flash("El monto es obligatorio.", "error")
            return redirect(url_for("finanzas.registrar_gasto"))

        try:
            monto = float(monto)

            if monto <= 0:
                flash("El monto debe ser mayor que 0.", "error")
                return redirect(url_for("finanzas.registrar_gasto"))

        except ValueError:
            flash("El monto ingresado no es válido.", "error")
            return redirect(url_for("finanzas.registrar_gasto"))

        # Validar categoría
        if not categoria:
            flash("Debe seleccionar una categoría.", "error")
            return redirect(url_for("finanzas.registrar_gasto"))

        # Validar fecha
        if not fecha:
            flash("La fecha es obligatoria.", "error")
            return redirect(url_for("finanzas.registrar_gasto"))

        # Guardar en MySQL
        success, message = gastos.registrar_gasto(
            concepto,
            monto,
            categoria,
            fecha,
            descripcion
        )

        if success:
            flash(message, "success")
        else:
            flash(message, "error")

        return redirect(url_for("finanzas.registrar_gasto"))

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

    conn = None
    cursor = None

    try:
        conn = mysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # =========================
        # TOTAL INGRESOS
        # =========================
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM ingresos
        """)

        total_ingresos = cursor.fetchone()[0]


        # =========================
        # TOTAL GASTOS
        # =========================
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM gastos
        """)

        total_gastos = cursor.fetchone()[0]


    except Exception as e:

        print(f"Error al consultar balance general: {e}")

        total_ingresos = 0
        total_gastos = 0


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


    return render_template(
        "finanzas/balance_general.html",
        total_ingresos=total_ingresos,
        total_gastos=total_gastos
    )