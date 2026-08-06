from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from auth import login_required, superadmin_required

from models.empresa import (
    registrarEmpresa,
    obtenerEmpresas,
    obtenerEmpresaID,
    actualizarEmpresa,
    activarEmpresa,
    desactivarEmpresa
)

empresas_bp = Blueprint("empresas", __name__)


# ==========================================
# EMPRESAS (LISTAR + REGISTRAR + EDITAR)
# ==========================================

@empresas_bp.route("/empresas", methods=["GET", "POST"])
@login_required
@superadmin_required
def empresas():

    empresa = None

    # -------------------------
    # EDITAR
    # -------------------------

    id_empresa = request.args.get("editar")

    if id_empresa:

        empresa = obtenerEmpresaID(id_empresa)

        if empresa is None:

            flash("Empresa no encontrada.", "error")

            return redirect(url_for("empresas.empresas"))

    # -------------------------
    # GUARDAR
    # -------------------------

    if request.method == "POST":

        id_empresa = request.form.get("id_empresa")

        if id_empresa:

            ok, mensaje = actualizarEmpresa(

                id_empresa,

                request.form["nombre"],

                request.form["nit"],

                request.form["direccion"],

                request.form["telefono"],

                request.form.get("estado", 1)

            )

        else:

            ok, mensaje = registrarEmpresa(

                request.form["nombre"],

                request.form["nit"],

                request.form["direccion"],

                request.form["telefono"],

                1

            )

        flash(

            mensaje,

            "success" if ok else "error"

        )

        return redirect(url_for("empresas.empresas"))

    empresas = obtenerEmpresas()

    return render_template(

        "empresas/empresas.html",

        empresas=empresas,

        empresa=empresa

    )


# ==========================================
# ACTIVAR
# ==========================================

@empresas_bp.route("/activar_empresa/<int:id_empresa>")
@login_required
@superadmin_required
def activar_empresa(id_empresa):

    ok, mensaje = activarEmpresa(id_empresa)

    flash(

        mensaje,

        "success" if ok else "error"

    )

    return redirect(url_for("empresas.empresas"))


# ==========================================
# DESACTIVAR
# ==========================================

@empresas_bp.route("/desactivar_empresa/<int:id_empresa>")
@login_required
@superadmin_required
def desactivar_empresa(id_empresa):

    ok, mensaje = desactivarEmpresa(id_empresa)

    flash(

        mensaje,

        "success" if ok else "error"

    )

    return redirect(url_for("empresas.empresas"))