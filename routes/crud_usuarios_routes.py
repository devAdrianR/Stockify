from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from auth import login_required, superadmin_required

from models.crud_usuarios import (
    obtenerUsuarios,
    obtenerUsuarioID,
    registrarUsuario,
    actualizarUsuario,
    activarUsuario,
    desactivarUsuario,
    obtenerEmpresas
)

crud_usuarios_bp = Blueprint("crud_usuarios", __name__)


@crud_usuarios_bp.route("/usuarios", methods=["GET", "POST"])
@login_required
@superadmin_required
def usuarios():

    usuario = None

    id_editar = request.args.get("editar")

    if id_editar:

        usuario = obtenerUsuarioID(id_editar)

    if request.method == "POST":

        id_usuario = request.form.get("id_usuario")
        id_empresa = request.form.get("id_empresa")

        if not id_empresa:

            flash(

                "Debe seleccionar una empresa.",

                "error"

            )

            return redirect(

                url_for("crud_usuarios.usuarios")

            )

        if id_usuario:

            ok, mensaje = actualizarUsuario(

                id_usuario,

                request.form["nombre_usuario"],

                request.form["correo"],

                request.form.get("password", ""),

                request.form["rol"],

                request.form.get("id_empresa"),

                request.form["estado"]

            )

        else:

            ok, mensaje = registrarUsuario(

                request.form["nombre_usuario"],

                request.form["correo"],

                request.form["password"],

                request.form["rol"],

                request.form.get("id_empresa")

            )

        flash(

            mensaje,

            "success" if ok else "error"

        )

        return redirect(

            url_for("crud_usuarios.usuarios")

        )

    return render_template(

        "empresas/usuarios.html",

        usuarios=obtenerUsuarios(),

        empresas=obtenerEmpresas(),

        usuario=usuario

    )


@crud_usuarios_bp.route("/activar_usuario/<int:id_usuario>")
@login_required
@superadmin_required
def activar_usuario(id_usuario):

    ok, mensaje = activarUsuario(id_usuario)

    flash(

        "success" if ok else "error"

    )

    return redirect(

        url_for("crud_usuarios.usuarios")

    )


@crud_usuarios_bp.route("/desactivar_usuario/<int:id_usuario>")
@login_required
@superadmin_required
def desactivar_usuario(id_usuario):

    ok, mensaje = desactivarUsuario(id_usuario)

    flash(

        mensaje,

        "success" if ok else "error"

    )

    return redirect(

        url_for("crud_usuarios.usuarios")

    )