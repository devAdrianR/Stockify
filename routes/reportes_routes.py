from flask import Blueprint, render_template, request, session, jsonify
from auth import login_required

from models.reportes import (
    resumenReportes,
    ventasDiarias,
    resumenVentasDiarias,
    detalleVenta
)

reportes_bp = Blueprint("reportes", __name__)


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

    resumen = resumenReportes(id_empresa)

    return render_template(
        "reportes/reportes.html",
        resumen=resumen
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

    # ==========================================
    # FECHA SELECCIONADA
    # ==========================================

    fecha = request.args.get("fecha")

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
        fecha=fecha
    )


# =====================================================
# DETALLE DE UNA VENTA - AJAX
# =====================================================

@reportes_bp.route("/reportes/detalle_venta/<int:id_venta>")
@login_required
def detalle_venta(id_venta):

    id_empresa = session.get("id_empresa")

    if id_empresa is None:
        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada."
        }), 400

    # ==========================================
    # OBTENER DETALLE
    # ==========================================

    encabezado, productos = detalleVenta(
        id_empresa,
        id_venta
    )

    # ==========================================
    # VENTA NO ENCONTRADA
    # ==========================================

    if encabezado is None:
        return jsonify({
            "ok": False,
            "mensaje": "Venta no encontrada."
        }), 404

    # ==========================================
    # RESPUESTA JSON
    # ==========================================

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

    id_empresa = session.get("id_empresa")

    if id_empresa is None:
        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada."
        }), 400

    resumen = resumenReportes(id_empresa)

    return render_template(
        "reportes/ventas_mensuales.html",
        resumen=resumen
    )


# =====================================================
# PRODUCTOS MÁS VENDIDOS
# =====================================================

@reportes_bp.route("/reportes/productos_mas_vendidos")
@login_required
def productos_mas_vendidos():

    id_empresa = session.get("id_empresa")

    if id_empresa is None:
        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada."
        }), 400

    resumen = resumenReportes(id_empresa)

    return render_template(
        "reportes/productos_mas_vendidos.html",
        resumen=resumen
    )


# =====================================================
# UTILIDAD POR PRODUCTO
# =====================================================

@reportes_bp.route("/reportes/utilidad_productos")
@login_required
def utilidad_productos():

    id_empresa = session.get("id_empresa")

    if id_empresa is None:
        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada."
        }), 400

    resumen = resumenReportes(id_empresa)

    return render_template(
        "reportes/utilidad_productos.html",
        resumen=resumen
    )


# =====================================================
# PRODUCTOS SIN MOVIMIENTO
# =====================================================

@reportes_bp.route("/reportes/productos_sin_movimiento")
@login_required
def productos_sin_movimiento():

    id_empresa = session.get("id_empresa")

    if id_empresa is None:
        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa asociada."
        }), 400

    resumen = resumenReportes(id_empresa)

    return render_template(
        "reportes/productos_sin_movimiento.html",
        resumen=resumen
    )