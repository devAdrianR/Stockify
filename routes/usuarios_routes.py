from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from auth import login_required, admin_required

from models.usuarios import (
    registrarUsuario,
    obtenerUsuarios,
    obtenerUsuarioID,
    actualizarUsuario,
    cambiarPassword,
    activarUsuario,
    desactivarUsuario
)

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/registro_usuario")
@login_required
@admin_required
def registro_usuario():

    usuarios = obtenerUsuarios()

    return render_template(
        "usuarios/registro_usuario.html",
        usuarios=usuarios,
        usuarioEditar=None
    )


@usuarios_bp.route("/registrar_usuario", methods=["POST"])
@login_required
@admin_required
def registrar():

    usuario = request.form["usuario"].strip()
    correo = request.form["correo"].strip()
    password = request.form["password"]
    confirmar = request.form["confirmar"]
    rol = request.form["rol"]

    if password != confirmar:
        flash("Las contraseñas no coinciden.", "error")
        return redirect(url_for("usuarios.registro_usuario"))

    ok, mensaje = registrarUsuario(usuario, correo, password, rol)

    flash(mensaje, "success" if ok else "error")

    return redirect(url_for("usuarios.registro_usuario"))


@usuarios_bp.route("/editar_usuario/<int:id_usuario>")
@login_required
@admin_required
def editar_usuario(id_usuario):

    usuarioEditar = obtenerUsuarioID(id_usuario)

    if usuarioEditar is None:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("usuarios.registro_usuario"))

    usuarios = obtenerUsuarios()

    return render_template(
        "usuarios/registro_usuario.html",
        usuarios=usuarios,
        usuarioEditar=usuarioEditar
    )


@usuarios_bp.route("/actualizar_usuario", methods=["POST"])
@login_required
@admin_required
def actualizar_usuario():
    idUsuario = int(request.form["id_usuario"])

    if idUsuario == session["id_usuario"] and request.form["rol"] != "Administrador":
        flash("No puedes cambiar tu propio rol.", "error")
        return redirect(url_for("usuarios.registro_usuario"))

    idUsuario = request.form["id_usuario"]
    usuario = request.form["usuario"].strip()
    correo = request.form["correo"].strip()
    rol = request.form["rol"]
    estado = request.form["estado"]

    ok, mensaje = actualizarUsuario(
        idUsuario,
        usuario,
        correo,
        rol,
        estado
    )

    flash(mensaje, "success" if ok else "error")

    return redirect(url_for("usuarios.registro_usuario"))


@usuarios_bp.route("/activar_usuario/<int:id_usuario>")
@login_required
@admin_required
def activar_usuario(id_usuario):

    ok, mensaje = activarUsuario(id_usuario)

    flash(mensaje, "success" if ok else "error")

    return redirect(url_for("usuarios.registro_usuario"))


@usuarios_bp.route("/desactivar_usuario/<int:id_usuario>")
@login_required
@admin_required
def desactivar_usuario(id_usuario):

    if id_usuario == session["id_usuario"]:
        flash("No puedes desactivar tu propia cuenta.", "error")
        return redirect(url_for("usuarios.registro_usuario"))

    ok, mensaje = desactivarUsuario(id_usuario)

    flash(mensaje, "success" if ok else "error")

    return redirect(url_for("usuarios.registro_usuario"))


@usuarios_bp.route("/cambiar_password/<int:id_usuario>", methods=["GET", "POST"])
@login_required
@admin_required
def cambiar_password(id_usuario):

    usuario = obtenerUsuarioID(id_usuario)

    if usuario is None:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("usuarios.registro_usuario"))

    if request.method == "POST":

        password = request.form["password"]
        confirmar = request.form["confirmar"]

        if password != confirmar:
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for("usuarios.cambiar_password", id_usuario=id_usuario))

        ok, mensaje = cambiarPassword(id_usuario, password)

        flash(mensaje, "success" if ok else "error")

        return redirect(url_for("usuarios.registro_usuario"))

    return render_template(
        "usuarios/cambiar_password.html",
        usuario=usuario
    )