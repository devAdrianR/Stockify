from flask import Blueprint, render_template, request, jsonify, session
from auth import login_required

from models.ventas import (
    buscarProductoVenta,
    registrarVenta
)

ventas_bp = Blueprint("ventas", __name__)


# ======================================
# VISTA PRINCIPAL
# ======================================

@ventas_bp.route("/ventas")
@login_required
def ventas():

    return render_template("ventas/ventas.html")


# ======================================
# BUSCAR PRODUCTOS
# ======================================

@ventas_bp.route("/buscar_producto")
@login_required
def buscar_producto():

    texto = request.args.get("q", "").strip()

    if texto == "":
        return jsonify([])

    id_empresa = session.get("id_empresa")

    ok, mensaje, productos = buscarProductoVenta(
        texto,
        id_empresa
    )

    if ok:
        return jsonify(productos)

    return jsonify([])



# ======================================
# REGISTRAR VENTA
# ======================================

@ventas_bp.route("/registrar_venta", methods=["POST"])
@login_required
def registrar_venta():

    data = request.get_json()

    if not data:

        return jsonify({
            "ok": False,
            "mensaje": "No se recibieron datos."
        })

    id_usuario = session["id_usuario"]
    id_empresa = session.get("id_empresa")

    if not id_empresa:
        return jsonify({
            "ok": False,
            "mensaje": "No se encontró la empresa del usuario en sesión."
        })

    ok, mensaje = registrarVenta(

        id_empresa,

        id_usuario,

        data["cliente"],

        data["documento"],

        data["fecha"],

        data["metodo_pago"],

        data["subtotal"],

        data["descuento"],

        data["iva"],

        data["total"],

        data["observaciones"],

        data["productos"]

    )

    return jsonify({

        "ok": ok,

        "mensaje": mensaje

    })