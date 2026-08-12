from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from auth import login_required

from models.finanzas import (
    registrarIngreso,
    registrarGasto,
    resumenFinanzas,
    obtenerBalanceGeneral,
    obtenerIngresos,
    obtenerGastos
)


finanzas_bp = Blueprint("finanzas", __name__)


# =====================================================
# FINANZAS
# =====================================================

@finanzas_bp.route("/finanzas")
@login_required
def finanzas():

    id_empresa = session.get("id_empresa")

    if not id_empresa:

        flash(
            "No se pudo identificar la empresa.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )

    # ==============================================
    # OBTENER RESUMEN
    # ==============================================

    resumen = resumenFinanzas(id_empresa)

    # ==============================================
    # MOSTRAR FINANZAS
    # ==============================================

    return render_template(
        "finanzas/finanzas.html",

        ingresos_dia=resumen["ingresos_dia"],

        gastos_dia=resumen["gastos_dia"],

        utilidad=resumen["utilidad"],

        saldo_caja=resumen["saldo_caja"]
    )


# =====================================================
# REGISTRAR INGRESO
# =====================================================

@finanzas_bp.route(
    "/registrar_ingreso",
    methods=["GET", "POST"]
)
@login_required
def registrar_ingreso():

    if request.method == "POST":

        # ==============================================
        # DATOS DEL FORMULARIO
        # ==============================================

        concepto = request.form["concepto"].strip()

        monto = request.form["monto"]

        categoria = request.form["categoria"]

        fecha = request.form["fecha"]

        descripcion = request.form.get(
            "descripcion",
            ""
        ).strip()

        # ==============================================
        # SESIÓN
        # ==============================================

        id_empresa = session.get("id_empresa")

        id_usuario = session.get("id_usuario")

        if not id_empresa or not id_usuario:

            flash(
                "No se pudo identificar el usuario o la empresa.",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        # ==============================================
        # REGISTRAR MEDIANTE EL MODEL
        # ==============================================

        correcto, mensaje = registrarIngreso(

            id_empresa,

            id_usuario,

            concepto,

            monto,

            categoria,

            fecha,

            descripcion
        )

        # ==============================================
        # RESULTADO
        # ==============================================

        if correcto:

            flash(
                mensaje,
                "success"
            )

            return redirect(
                url_for("finanzas.finanzas")
            )

        else:

            flash(
                mensaje,
                "error"
            )

    # ==============================================
    # MOSTRAR FORMULARIO
    # ==============================================

    return render_template(
        "finanzas/registrar_ingreso.html"
    )


# =====================================================
# REGISTRAR GASTO
# =====================================================

@finanzas_bp.route(
    "/registrar_gasto",
    methods=["GET", "POST"]
)
@login_required
def registrar_gasto():

    if request.method == "POST":

        # ==============================================
        # SESIÓN
        # ==============================================

        id_empresa = session.get("id_empresa")

        id_usuario = session.get("id_usuario")

        if not id_empresa or not id_usuario:

            flash(
                "No se pudo identificar el usuario o la empresa.",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        # ==============================================
        # DATOS DEL FORMULARIO
        # ==============================================

        concepto = request.form["concepto"].strip()

        monto = request.form["monto"]

        categoria = request.form["categoria"]

        fecha = request.form["fecha"]

        descripcion = request.form.get(
            "descripcion",
            ""
        ).strip()

        # ==============================================
        # REGISTRAR MEDIANTE EL MODEL
        # ==============================================

        correcto, mensaje = registrarGasto(

            id_empresa,

            id_usuario,

            concepto,

            categoria,

            monto,

            fecha,

            descripcion
        )

        # ==============================================
        # RESULTADO
        # ==============================================

        if correcto:

            flash(
                mensaje,
                "success"
            )

            return redirect(
                url_for("finanzas.finanzas")
            )

        else:

            flash(
                mensaje,
                "error"
            )

    # ==============================================
    # MOSTRAR FORMULARIO
    # ==============================================

    return render_template(
        "finanzas/registrar_gasto.html"
    )


# =====================================================
# BALANCE GENERAL
# =====================================================

@finanzas_bp.route("/balance_general")
@login_required
def balance_general():

    id_empresa = session.get("id_empresa")

    if not id_empresa:

        flash(
            "No se pudo identificar la empresa.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )

    # ==============================================
    # OBTENER BALANCE DESDE EL MODEL
    # ==============================================

    balance = obtenerBalanceGeneral(
        id_empresa
    )

    # ==============================================
    # MOSTRAR BALANCE
    # ==============================================

    return render_template(
        "finanzas/balance_general.html",

        total_ingresos=balance["total_ingresos"],

        total_gastos=balance["total_gastos"],

        cuentas_cobrar=balance["cuentas_cobrar"],

        cuentas_pagar=balance["cuentas_pagar"],

        utilidad_neta=balance["utilidad_neta"]
    )