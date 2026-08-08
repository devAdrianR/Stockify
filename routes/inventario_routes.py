from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from auth import login_required

from models.productos import (
    obtenerProducto,
    registrarProducto,
    editarProducto,
    activarProducto,
    desactivarProducto,
    categorias,
    buscarProducto
)

inventario_bp = Blueprint("inventario", __name__)


def get_id_empresa():
    id_empresa = session.get("id_empresa")

    if id_empresa is None:
        flash("No se encontró la empresa asociada al usuario.", "error")

    return id_empresa


@inventario_bp.route("/inventario")
@login_required
def inventario():
    return redirect(url_for("inventario.registrar_producto"))


# ==========================================
# REGISTRAR PRODUCTO + LISTAR PRODUCTOS
# ==========================================

@inventario_bp.route("/registrar_producto", methods=["GET", "POST"])
@login_required
def registrar_producto():

    id_empresa = get_id_empresa()

    if id_empresa is None:
        return redirect(url_for("inventario.registrar_producto"))

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        codigo = request.form["codigo"].strip()
        categoria = request.form["categoria"].strip()
        costo = request.form["costo"]
        precio_venta = request.form["precio_venta"]
        stock = request.form["stock"]
        descripcion = request.form["descripcion"].strip()

        ok, mensaje = registrarProducto(

            id_empresa,
            nombre,
            codigo,
            categoria,
            costo,
            precio_venta,
            stock,
            descripcion

        )

        flash(mensaje, "success" if ok else "error")

        return redirect(url_for("inventario.registrar_producto"))

    ok, mensaje, productos = obtenerProducto(id_empresa=id_empresa)

    if not ok:
        productos = []

    return render_template(
        "inventario/registrar_producto.html",
        productos=productos,
        productoEditar=None
    )


# ==========================================
# BUSCAR PRODUCTOS
# ==========================================

@inventario_bp.route("/buscar_productos")
@login_required
def buscar_productos():

    id_empresa = get_id_empresa()

    if id_empresa is None:
        return {
            "ok": False,
            "productos": []
        }

    texto = request.args.get("texto", "").strip()
    filtro = request.args.get("filtro", "todos")

    ok, mensaje, productos = buscarProducto(

        id_empresa,
        texto,
        filtro

    )

    return {
        "ok": ok,
        "productos": productos
    }


# ==========================================
# EDITAR PRODUCTO
# ==========================================

@inventario_bp.route("/editar_producto/<int:id_producto>")
@login_required
def editar_producto(id_producto):

    id_empresa = get_id_empresa()

    if id_empresa is None:
        return redirect(url_for("inventario.registrar_producto"))

    ok, _, productoEditar = obtenerProducto(

        id_empresa,
        id_producto

    )

    ok_lista, _, productos = obtenerProducto(id_empresa=id_empresa)

    if not ok_lista:
        productos = []

    if not ok:
        flash("No se encontró el producto solicitado.", "error")
        return redirect(url_for("inventario.registrar_producto"))

    return render_template(
        "inventario/registrar_producto.html",
        productoEditar=productoEditar,
        productos=productos
    )


# ==========================================
# ACTUALIZAR PRODUCTO
# ==========================================

@inventario_bp.route("/actualizar_producto", methods=["POST"])
@login_required
def actualizar_producto():

    id_empresa = get_id_empresa()

    if id_empresa is None:
        return redirect(url_for("inventario.registrar_producto"))

    id_producto = request.form["id_producto"]

    nombre = request.form["nombre"].strip()
    codigo = request.form["codigo"].strip()
    categoria = request.form["categoria"].strip()
    costo = request.form["costo"]
    precio_venta = request.form["precio_venta"]
    stock = request.form["stock"]
    descripcion = request.form["descripcion"].strip()
    estado = request.form["estado"]

    ok, mensaje = editarProducto(

        id_empresa,
        id_producto,
        nombre,
        codigo,
        categoria,
        costo,
        precio_venta,
        stock,
        descripcion,
        estado

    )

    flash(mensaje, "success" if ok else "error")

    return redirect(url_for("inventario.registrar_producto"))


# ==========================================
# ACTIVAR PRODUCTO
# ==========================================

@inventario_bp.route("/activar_producto/<int:id_producto>")
@login_required
def activar_producto(id_producto):

    id_empresa = get_id_empresa()

    if id_empresa is None:
        return redirect(url_for("inventario.registrar_producto"))

    ok, mensaje = activarProducto(

        id_empresa,
        id_producto

    )

    flash(mensaje, "success" if ok else "error")

    return redirect(url_for("inventario.registrar_producto"))


# ==========================================
# DESACTIVAR PRODUCTO
# ==========================================

@inventario_bp.route("/desactivar_producto/<int:id_producto>")
@login_required
def desactivar_producto(id_producto):

    id_empresa = get_id_empresa()

    if id_empresa is None:
        return redirect(url_for("inventario.registrar_producto"))

    ok, mensaje = desactivarProducto(

        id_empresa,
        id_producto

    )

    flash(mensaje, "success" if ok else "error")

    return redirect(url_for("inventario.registrar_producto"))


# ==========================================
# CATEGORÍAS
# ==========================================

@inventario_bp.route("/categorias")
@login_required
def ver_categorias():

    id_empresa = get_id_empresa()

    if id_empresa is None:
        return redirect(url_for("inventario.registrar_producto"))

    ok, mensaje, lista_categorias = categorias(id_empresa)

    if ok:

        return render_template(
            "inventario/categorias.html",
            categorias=lista_categorias
        )

    flash(mensaje, "error")

    return redirect(url_for("inventario.registrar_producto"))