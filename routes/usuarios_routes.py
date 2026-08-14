from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

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

from models.dashboard import obtenerEmpresa


usuarios_bp = Blueprint(
    "usuarios",
    __name__
)


# ==========================================================
# REGISTRO / LISTADO DE USUARIOS
# ==========================================================

@usuarios_bp.route("/registro_usuario")
@login_required
@admin_required
def registro_usuario():

    usuarios = obtenerUsuarios()

    rol = session.get("rol")

    empresa = None

    # El ADMIN debe tener empresa
    if rol == "ADMIN":

        id_empresa = session.get("id_empresa")

        if not id_empresa:

            session.clear()

            return redirect(
                url_for("auth.login")
            )

        empresa = obtenerEmpresa(
            id_empresa
        )

        if empresa is None:

            session.clear()

            return redirect(
                url_for("auth.login")
            )

    return render_template(
        "usuarios/registro_usuario.html",
        usuarios=usuarios,
        usuarioEditar=None,
        empresa=empresa
    )


# ==========================================================
# REGISTRAR USUARIO
# ==========================================================

@usuarios_bp.route(
    "/registrar_usuario",
    methods=["POST"]
)
@login_required
@admin_required
def registrar():

    usuario = request.form["usuario"].strip()
    correo = request.form["correo"].strip()
    password = request.form["password"]
    confirmar = request.form["confirmar"]
    rol = request.form["rol"]

    # Validar contraseñas
    if password != confirmar:

        flash(
            "Las contraseñas no coinciden.",
            "error"
        )

        return redirect(
            url_for("usuarios.registro_usuario")
        )

    # Obtener empresa del usuario administrador
    id_empresa = session.get("id_empresa")

    if not id_empresa:

        flash(
            "El administrador no tiene una empresa asignada.",
            "error"
        )

        return redirect(
            url_for("usuarios.registro_usuario")
        )

    # Registrar usuario
    ok, mensaje = registrarUsuario(
        id_empresa,
        usuario,
        correo,
        password,
        rol
    )

    flash(
        mensaje,
        "success" if ok else "error"
    )

    return redirect(
        url_for("usuarios.registro_usuario")
    )


# ==========================================================
# EDITAR USUARIO
# ==========================================================

@usuarios_bp.route(
    "/editar_usuario/<int:id_usuario>"
)
@login_required
@admin_required
def editar_usuario(id_usuario):

    usuarioEditar = obtenerUsuarioID(
        id_usuario
    )

    if usuarioEditar is None:

        flash(
            "Usuario no encontrado.",
            "error"
        )

        return redirect(
            url_for("usuarios.registro_usuario")
        )

    usuarios = obtenerUsuarios()

    rol = session.get("rol")

    empresa = None

    # El ADMIN debe tener empresa
    if rol == "ADMIN":

        id_empresa = session.get("id_empresa")

        if not id_empresa:

            session.clear()

            return redirect(
                url_for("auth.login")
            )

        empresa = obtenerEmpresa(
            id_empresa
        )

        if empresa is None:

            session.clear()

            return redirect(
                url_for("auth.login")
            )

    return render_template(
        "usuarios/registro_usuario.html",
        usuarios=usuarios,
        usuarioEditar=usuarioEditar,
        empresa=empresa
    )


# ==========================================================
# ACTUALIZAR USUARIO
# ==========================================================

@usuarios_bp.route(
    "/actualizar_usuario",
    methods=["POST"]
)
@login_required
@admin_required
def actualizar_usuario():

    idUsuario = int(
        request.form["id_usuario"]
    )

    usuario = request.form["usuario"].strip()
    correo = request.form["correo"].strip()
    rol = request.form["rol"]
    estado = request.form["estado"]

    # No permitir que el administrador cambie
    # su propio rol
    if (
        idUsuario == session["id_usuario"]
        and rol != "Administrador"
    ):

        flash(
            "No puedes cambiar tu propio rol.",
            "error"
        )

        return redirect(
            url_for("usuarios.registro_usuario")
        )

    ok, mensaje = actualizarUsuario(
        idUsuario,
        usuario,
        correo,
        rol,
        estado
    )

    flash(
        mensaje,
        "success" if ok else "error"
    )

    return redirect(
        url_for("usuarios.registro_usuario")
    )


# ==========================================================
# CAMBIAR CONTRASEÑA
# ==========================================================

@usuarios_bp.route(
    "/cambiar_password/<int:id_usuario>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def cambiar_password(id_usuario):

    usuario = obtenerUsuarioID(
        id_usuario
    )

    if usuario is None:

        flash(
            "Usuario no encontrado.",
            "error"
        )

        return redirect(
            url_for("usuarios.registro_usuario")
        )

    rol = session.get("rol")

    empresa = None

    # El ADMIN debe tener empresa
    if rol == "ADMIN":

        id_empresa = session.get("id_empresa")

        if not id_empresa:

            session.clear()

            return redirect(
                url_for("auth.login")
            )

        empresa = obtenerEmpresa(
            id_empresa
        )

        if empresa is None:

            session.clear()

            return redirect(
                url_for("auth.login")
            )

    # Si enviaron el formulario
    if request.method == "POST":

        password = request.form["password"]
        confirmar = request.form["confirmar"]

        # Validar contraseñas
        if password != confirmar:

            flash(
                "Las contraseñas no coinciden.",
                "error"
            )

            return redirect(
                url_for(
                    "usuarios.cambiar_password",
                    id_usuario=id_usuario
                )
            )

        ok, mensaje = cambiarPassword(
            id_usuario,
            password
        )

        flash(
            mensaje,
            "success" if ok else "error"
        )

        return redirect(
            url_for("usuarios.registro_usuario")
        )

    # Mostrar formulario
    return render_template(
        "usuarios/cambiar_password.html",
        usuario=usuario,
        empresa=empresa
    )


# ==========================================================
# ACTIVAR USUARIO
# ==========================================================

@usuarios_bp.route(
    "/activar_usuario/<int:id_usuario>"
)
@login_required
@admin_required
def activar_usuario(id_usuario):

    ok, mensaje = activarUsuario(
        id_usuario
    )

    flash(
        mensaje,
        "success" if ok else "error"
    )

    return redirect(
        url_for("usuarios.registro_usuario")
    )


# ==========================================================
# DESACTIVAR USUARIO
# ==========================================================

@usuarios_bp.route(
    "/desactivar_usuario/<int:id_usuario>"
)
@login_required
@admin_required
def desactivar_usuario(id_usuario):

    if id_usuario == session["id_usuario"]:

        flash(
            "No puedes desactivar tu propia cuenta.",
            "error"
        )

        return redirect(
            url_for("usuarios.registro_usuario")
        )

    ok, mensaje = desactivarUsuario(
        id_usuario
    )

    flash(
        mensaje,
        "success" if ok else "error"
    )

    return redirect(
        url_for("usuarios.registro_usuario")
    )