from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from auth import login_required
from models.productos import registrarProducto, editarProducto, eliminarProducto, verInventario, categorias, movimientos

inventario_bp = Blueprint("inventario", __name__)

@inventario_bp.route("/inventario")
@login_required
def inventario():
    return render_template("inventario/inventario.html")

@inventario_bp.route("/registrar_producto", methods=["GET", "POST"])
@login_required
def registrar_producto():

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        codigo = request.form["codigo"].strip()
        categoria = request.form["categoria"].strip()
        costo = request.form["costo"]
        precio_venta = request.form["precio_venta"]
        stock = request.form["stock"]
        descripcion = request.form["descripcion"].strip()

        ok, mensaje = registrarProducto(
            nombre,
            codigo,
            categoria,
            costo,
            precio_venta,
            stock,
            descripcion
        )

        flash(mensaje, "success" if ok else "error")

        if ok:
            return redirect(url_for("inventario.registrar_producto"))

    return render_template("inventario/registrar_producto.html")

@inventario_bp.route("/editar_producto", methods=["GET", "POST"])
@login_required
def editar_producto():
    if request.method == "POST":
        id_producto = request.form["id_producto"]
        nombre = request.form["nombre"].strip()
        codigo = request.form["codigo"].strip()
        categoria = request.form["categoria"].strip()
        costo = request.form["costo"]
        precio_venta = request.form["precio_venta"]
        stock = request.form["stock"]
        descripcion = request.form["descripcion"].strip()

        ok, mensaje = editarProducto(
            id_producto,
            nombre,
            codigo,
            categoria,
            costo,
            precio_venta,
            stock,
            descripcion
        )

        flash(mensaje, "success" if ok else "error")

        if ok:
            return redirect(url_for("inventario.inventario"))

    return render_template("inventario/editar_producto.html")

@inventario_bp.route("/eliminar_producto", methods=["GET", "POST"])
@login_required
def eliminar_producto():
    if request.method == "POST":
        id_producto = request.form["id_producto"]
        ok, mensaje = eliminarProducto(id_producto)
        flash(mensaje, "success" if ok else "error")
        if ok:
            return redirect(url_for("inventario.inventario"))
    return render_template("inventario/eliminar_producto.html")

@inventario_bp.route("/ver_inventario")
@login_required
def ver_inventario():
    ok, mensaje, productos = verInventario()
    if ok:
        return render_template("inventario/ver_inventario.html", productos=productos)
    else:
        flash(mensaje, "error")
        return redirect(url_for("inventario.inventario"))

@inventario_bp.route("/categorias")
@login_required
def categorias():
    ok, mensaje, categorias = categorias()
    if ok:
        return render_template("inventario/categorias.html", categorias=categorias)
    else:
        flash(mensaje, "error")
        return redirect(url_for("inventario.inventario"))

@inventario_bp.route("/movimientos")
@login_required
def movimientos():
    ok, mensaje, movimientos = movimientos()
    if ok:
        return render_template("inventario/movimientos.html", movimientos=movimientos)
    else:
        flash(mensaje, "error")
        return redirect(url_for("inventario.inventario"))
