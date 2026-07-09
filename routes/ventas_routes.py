from flask import Blueprint, render_template, request, jsonify
from auth import login_required

from models.ventas import buscarProductoVenta

ventas_bp = Blueprint("ventas", __name__)


@ventas_bp.route("/ventas")
@login_required
def ventas():
    return render_template("ventas/ventas.html")


# ======================================
# BUSCAR PRODUCTOS (AJAX)
# ======================================

@ventas_bp.route("/buscar_producto")
@login_required
def buscar_producto():

    texto = request.args.get("q", "").strip()

    if texto == "":
        return jsonify([])

    ok, mensaje, productos = buscarProductoVenta(texto)

    if ok:
        return jsonify(productos)

    return jsonify([])