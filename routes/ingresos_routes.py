from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import ingresos


ingresos_bp = Blueprint("ingresos", __name__)


@ingresos_bp.route("/registrar_ingreso", methods=["GET", "POST"])
def registrar_ingreso():

    if request.method == "POST":

        concepto = request.form.get("concepto", "").strip()
        monto = request.form.get("monto", "").strip()
        categoria = request.form.get("categoria", "").strip()
        fecha = request.form.get("fecha", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        # Validaciones
        if not concepto:
            flash("El concepto es obligatorio.", "error")
            return redirect(url_for("ingresos.registrar_ingreso"))

        if not monto:
            flash("El monto es obligatorio.", "error")
            return redirect(url_for("ingresos.registrar_ingreso"))

        if not categoria:
            flash("Debe seleccionar una categoría.", "error")
            return redirect(url_for("ingresos.registrar_ingreso"))

        if not fecha:
            flash("La fecha es obligatoria.", "error")
            return redirect(url_for("ingresos.registrar_ingreso"))

        try:
            monto = float(monto)

            if monto <= 0:
                flash("El monto debe ser mayor que 0.", "error")
                return redirect(url_for("ingresos.registrar_ingreso"))

        except ValueError:
            flash("El monto ingresado no es válido.", "error")
            return redirect(url_for("ingresos.registrar_ingreso"))

        # Registrar en la base de datos
        success, message = ingresos.registrar_ingreso(
            concepto,
            monto,
            categoria,
            fecha,
            descripcion
        )

        if success:
            flash(message, "success")
            return redirect(url_for("ingresos.registrar_ingreso"))

        flash(message, "error")
        return redirect(url_for("ingresos.registrar_ingreso"))

    return render_template("ingresos/registrar_ingreso.html")