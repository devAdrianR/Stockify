from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from auth import login_required
import mysql.connector
from config import DB_CONFIG

finanzas_bp = Blueprint("finanzas", __name__)


# ======================================
# FINANZAS
# ======================================

@finanzas_bp.route("/finanzas")
@login_required
def finanzas():

    id_usuario = session.get("id_usuario")
    id_empresa = session.get("id_empresa")

    if not id_usuario or not id_empresa:
        flash("No se pudo identificar el usuario o la empresa.", "error")
        return redirect(url_for("auth.login"))

    try:

        con = mysql.connector.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)

        # INGRESOS DEL DÍA
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) AS ingresos_dia
            FROM ingresos
            WHERE id_empresa = %s
            AND id_usuario = %s
            AND DATE(fecha) = CURDATE()
        """, (id_empresa, id_usuario))

        ingresos_dia = cursor.fetchone()["ingresos_dia"]


        # GASTOS DEL DÍA
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) AS gastos_dia
            FROM gastos
            WHERE id_empresa = %s
            AND id_usuario = %s
            AND DATE(fecha) = CURDATE()
        """, (id_empresa, id_usuario))

        gastos_dia = cursor.fetchone()["gastos_dia"]


        # UTILIDAD
        utilidad = ingresos_dia - gastos_dia


        # SALDO EN CAJA
        saldo_caja = utilidad


        cursor.close()
        con.close()


        return render_template(
            "finanzas/finanzas.html",
            ingresos_dia=ingresos_dia,
            gastos_dia=gastos_dia,
            utilidad=utilidad,
            saldo_caja=saldo_caja
        )


    except Exception as e:

        print("ERROR EN FINANZAS:", e)

        return render_template(
            "finanzas/finanzas.html",
            ingresos_dia=0,
            gastos_dia=0,
            utilidad=0,
            saldo_caja=0
        )


# ======================================
# REGISTRAR INGRESO
# ======================================

@finanzas_bp.route("/registrar_ingreso", methods=["GET", "POST"])
@login_required
def registrar_ingreso():

    if request.method == "POST":

        concepto = request.form["concepto"].strip()
        monto = request.form["monto"]
        categoria = request.form["categoria"]
        fecha = request.form["fecha"]
        descripcion = request.form.get("descripcion", "").strip()

        id_usuario = session.get("id_usuario")
        id_empresa = session.get("id_empresa")


        if not id_usuario or not id_empresa:

            flash("No se pudo identificar el usuario o la empresa.", "error")

            return redirect(url_for("auth.login"))


        try:

            con = mysql.connector.connect(**DB_CONFIG)
            cursor = con.cursor()

            cursor.execute("""
                INSERT INTO ingresos
                (
                    id_empresa,
                    id_usuario,
                    concepto,
                    monto,
                    categoria,
                    fecha,
                    descripcion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                id_empresa,
                id_usuario,
                concepto,
                monto,
                categoria,
                fecha,
                descripcion
            ))

            con.commit()

            cursor.close()
            con.close()

            flash("Ingreso registrado correctamente.", "success")

            return redirect(url_for("finanzas.finanzas"))


        except Exception as e:

            print("ERROR AL REGISTRAR INGRESO:", e)

            flash("No se pudo registrar el ingreso.", "error")


    return render_template("finanzas/registrar_ingreso.html")


# ======================================
# REGISTRAR GASTO
# ======================================

@finanzas_bp.route("/registrar_gasto", methods=["GET", "POST"])
@login_required
def registrar_gasto():

    if request.method == "POST":

        id_usuario = session.get("id_usuario")
        id_empresa = session.get("id_empresa")

        concepto = request.form["concepto"]
        monto = request.form["monto"]
        categoria = request.form["categoria"]
        fecha = request.form["fecha"]
        descripcion = request.form.get("descripcion", "")


        if not id_usuario or not id_empresa:

            flash("No se pudo identificar el usuario o la empresa.", "error")

            return redirect(url_for("auth.login"))


        try:

            con = mysql.connector.connect(**DB_CONFIG)
            cursor = con.cursor()

            cursor.execute("""
                INSERT INTO gastos
                (
                    id_empresa,
                    id_usuario,
                    concepto,
                    categoria,
                    monto,
                    fecha,
                    descripcion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                id_empresa,
                id_usuario,
                concepto,
                categoria,
                monto,
                fecha,
                descripcion
            ))

            con.commit()

            cursor.close()
            con.close()

            flash("Gasto registrado correctamente.", "success")

            return redirect(url_for("finanzas.finanzas"))


        except Exception as e:

            print("ERROR AL REGISTRAR GASTO:", e)

            flash("No se pudo registrar el gasto.", "error")


    return render_template("finanzas/registrar_gasto.html")


# ======================================
# CAJA DEL DÍA
# ======================================

@finanzas_bp.route("/caja_dia")
@login_required
def caja_dia():

    return render_template("finanzas/caja_dia.html")


# ======================================
# CUENTAS POR COBRAR
# ======================================

@finanzas_bp.route("/cuentas_cobrar")
@login_required
def cuentas_cobrar():

    return render_template("finanzas/cuentas_cobrar.html")


# ======================================
# CUENTAS POR PAGAR
# ======================================

@finanzas_bp.route("/cuentas_pagar")
@login_required
def cuentas_pagar():

    return render_template("finanzas/cuentas_pagar.html")


# ======================================
# BALANCE GENERAL
# ======================================

@finanzas_bp.route("/balance_general")
@login_required
def balance_general():

    id_usuario = session.get("id_usuario")
    id_empresa = session.get("id_empresa")


    if not id_usuario or not id_empresa:

        flash("No se pudo identificar el usuario o la empresa.", "error")

        return redirect(url_for("auth.login"))


    try:

        con = mysql.connector.connect(**DB_CONFIG)
        cursor = con.cursor(dictionary=True)


        # TOTAL INGRESOS

        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) AS total_ingresos
            FROM ingresos
            WHERE id_empresa = %s
            AND id_usuario = %s
        """, (id_empresa, id_usuario))

        total_ingresos = cursor.fetchone()["total_ingresos"]


        # TOTAL GASTOS

        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0) AS total_gastos
            FROM gastos
            WHERE id_empresa = %s
            AND id_usuario = %s
        """, (id_empresa, id_usuario))

        total_gastos = cursor.fetchone()["total_gastos"]


        utilidad_neta = total_ingresos - total_gastos


        cursor.close()
        con.close()


        return render_template(
            "finanzas/balance_general.html",
            total_ingresos=total_ingresos,
            total_gastos=total_gastos,
            cuentas_cobrar=0,
            cuentas_pagar=0,
            utilidad_neta=utilidad_neta
        )


    except Exception as e:

        print("ERROR EN BALANCE GENERAL:", e)

        return render_template(
            "finanzas/balance_general.html",
            total_ingresos=0,
            total_gastos=0,
            cuentas_cobrar=0,
            cuentas_pagar=0,
            utilidad_neta=0
        )