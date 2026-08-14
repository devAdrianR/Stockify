from flask import (
    Blueprint,
    render_template,
    request,
    session,
    jsonify
)

from auth import login_required

from models.dashboard import obtenerEmpresa

from models.reportes import (
    resumenReportes,
    ventasDiarias,
    resumenVentasDiarias,
    detalleVenta,
    productosMasVendidos
)


reportes_bp = Blueprint(
    "reportes",
    __name__
)


# =====================================================
# MENÚ PRINCIPAL DE REPORTES
# =====================================================

@reportes_bp.route("/reportes")
@login_required
def reportes():

    id_empresa = session.get("id_empresa")

    if id_empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada al usuario."
        }), 400


    empresa = obtenerEmpresa(
        id_empresa
    )


    if empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa."
        }), 404


    resumen = resumenReportes(
        id_empresa
    )


    resultado_productos = productosMasVendidos(
        id_empresa
    )


    resumen["producto_mas_vendido"] = (
        resultado_productos["resumen"]["producto_mas_vendido"]
    )


    return render_template(
        "reportes/reportes.html",

        resumen=resumen,

        empresa=empresa
    )


# =====================================================
# VENTAS DIARIAS
# =====================================================

@reportes_bp.route("/reportes/ventas_diarias")
@login_required
def ventas_diarias():

    id_empresa = session.get("id_empresa")

    if id_empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada al usuario."
        }), 400


    empresa = obtenerEmpresa(
        id_empresa
    )


    if empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa."
        }), 404


    # ==========================================
    # FECHA SELECCIONADA
    # ==========================================

    fecha = request.args.get(
        "fecha"
    )


    # Si no se selecciona una fecha,
    # automáticamente se utiliza HOY.

    if not fecha:

        from datetime import date

        fecha = date.today().isoformat()


    # ==========================================
    # RESUMEN DEL DÍA
    # ==========================================

    resumen = resumenVentasDiarias(
        id_empresa,
        fecha
    )


    # ==========================================
    # VENTAS DEL DÍA
    # ==========================================

    ventas = ventasDiarias(
        id_empresa,
        fecha
    )


    # ==========================================
    # MOSTRAR VISTA
    # ==========================================

    return render_template(
        "reportes/ventas_diarias.html",

        resumen=resumen,

        ventas=ventas,

        fecha=fecha,

        empresa=empresa
    )


# =====================================================
# DETALLE DE UNA VENTA - AJAX
# =====================================================

@reportes_bp.route(
    "/reportes/detalle_venta/<int:id_venta>"
)
@login_required
def detalle_venta(id_venta):

    id_empresa = session.get(
        "id_empresa"
    )


    if id_empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada."
        }), 400


    encabezado, productos = detalleVenta(
        id_empresa,
        id_venta
    )


    if encabezado is None:

        return jsonify({
            "ok": False,
            "mensaje": "Venta no encontrada."
        }), 404


    return jsonify({

        "ok": True,

        "venta": encabezado,

        "productos": productos

    })


# =====================================================
# VENTAS MENSUALES
# =====================================================

@reportes_bp.route("/reportes/ventas_mensuales")
@login_required
def ventas_mensuales():

    id_empresa = session.get(
        "id_empresa"
    )


    if id_empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada al usuario."
        }), 400


    empresa = obtenerEmpresa(
        id_empresa
    )


    if empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa."
        }), 404


    resumen = resumenReportes(
        id_empresa
    )


    return render_template(
        "reportes/ventas_mensuales.html",

        resumen=resumen,

        empresa=empresa
    )


# =====================================================
# PRODUCTOS MÁS VENDIDOS
# =====================================================

@reportes_bp.route(
    "/reportes/productos_mas_vendidos"
)
@login_required
def productos_mas_vendidos():

    id_empresa = session.get(
        "id_empresa"
    )


    if id_empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada al usuario."
        }), 400


    empresa = obtenerEmpresa(
        id_empresa
    )


    if empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa."
        }), 404


    # ==========================================
    # FECHAS
    # ==========================================

    fecha_inicio = request.args.get(
        "fecha_inicio"
    )

    fecha_fin = request.args.get(
        "fecha_fin"
    )


    # ==========================================
    # CONSULTAR REPORTE
    # ==========================================

    resultado = productosMasVendidos(
        id_empresa,
        fecha_inicio,
        fecha_fin
    )


    # ==========================================
    # DATOS
    # ==========================================

    resumen = resultado["resumen"]

    productos = resultado["productos"]


    # ==========================================
    # MOSTRAR VISTA
    # ==========================================

    return render_template(
        "reportes/productos_mas_vendidos.html",

        resumen=resumen,

        productos=productos,

        fecha_inicio=fecha_inicio,

        fecha_fin=fecha_fin,

        empresa=empresa
    )


# =====================================================
# PRODUCTOS SIN MOVIMIENTO
# =====================================================

@reportes_bp.route(
    "/reportes/productos_sin_movimiento"
)
@login_required
def productos_sin_movimiento():

    id_empresa = session.get(
        "id_empresa"
    )


    if id_empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada al usuario."
        }), 400


    empresa = obtenerEmpresa(
        id_empresa
    )


    if empresa is None:

        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa."
        }), 404


    resumen = resumenReportes(
        id_empresa
    )


    return render_template(
        "reportes/productos_sin_movimiento.html",

        resumen=resumen,

        empresa=empresa
    )